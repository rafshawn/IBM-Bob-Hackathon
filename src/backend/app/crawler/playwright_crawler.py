"""
Playwright-based web crawler with domain restriction
"""
import asyncio
from urllib.parse import urlparse, urljoin
from typing import List, Set, Dict, Any, Optional
from playwright.async_api import async_playwright, Page, Browser
from bs4 import BeautifulSoup

from app.config import settings


class WebCrawler:
    """
    Asynchronous web crawler using Playwright
    
    Features:
    - Domain restriction (only crawls same domain)
    - Depth limiting
    - Page limit
    - JavaScript rendering
    - Element extraction for SEO and accessibility
    """
    
    def __init__(
        self,
        base_url: str,
        max_pages: int = 50,
        max_depth: int = 3,
        timeout: int = 30000
    ):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.timeout = timeout
        
        self.visited_urls: Set[str] = set()
        self.pages_data: List[Dict[str, Any]] = []
    
    async def crawl(self) -> List[Dict[str, Any]]:
        """
        Start crawling from base URL
        
        Returns:
            List of page data dictionaries
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            try:
                await self._crawl_recursive(browser, self.base_url, depth=0)
            finally:
                await browser.close()
        
        return self.pages_data
    
    async def _crawl_recursive(
        self,
        browser: Browser,
        url: str,
        depth: int
    ):
        """
        Recursively crawl pages
        """
        # Check limits
        if depth > self.max_depth:
            return
        
        if len(self.visited_urls) >= self.max_pages:
            return
        
        # Normalize URL
        url = url.rstrip('/')
        
        # Check if already visited
        if url in self.visited_urls:
            return
        
        # Check domain restriction
        if not self._is_same_domain(url):
            return
        
        # Mark as visited
        self.visited_urls.add(url)
        
        # Crawl the page
        page_data = await self._crawl_page(browser, url)
        
        if page_data:
            self.pages_data.append(page_data)
            
            # Extract and crawl links
            links = page_data.get('links', [])
            
            for link in links:
                if len(self.visited_urls) >= self.max_pages:
                    break
                
                await self._crawl_recursive(browser, link, depth + 1)
    
    async def _crawl_page(
        self,
        browser: Browser,
        url: str
    ) -> Optional[Dict[str, Any]]:
        """
        Crawl a single page and extract data
        """
        page = await browser.new_page()
        
        try:
            # Navigate to page
            response = await page.goto(url, timeout=self.timeout, wait_until='networkidle')
            
            if not response or response.status >= 400:
                return None
            
            # Wait for content to load
            await page.wait_for_load_state('domcontentloaded')
            
            # Get page content
            content = await page.content()
            
            # Extract data
            page_data = await self._extract_page_data(page, url, content, response.status)
            
            return page_data
            
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")
            return None
        finally:
            await page.close()
    
    async def _extract_page_data(
        self,
        page: Page,
        url: str,
        html_content: str,
        status_code: int
    ) -> Dict[str, Any]:
        """
        Extract relevant data from page
        """
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Extract title
        title = await page.title()
        
        # Extract meta description
        meta_desc = None
        meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_desc_tag and hasattr(meta_desc_tag, 'get'):
            meta_desc = meta_desc_tag.get('content')
        
        # Extract all meta tags
        meta_tags = {}
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                meta_tags[name] = content
        
        # Extract headings
        h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all('h1')]
        
        # Extract images with alt text
        images = []
        for img in soup.find_all('img'):
            images.append({
                'src': img.get('src'),
                'alt': img.get('alt', ''),
                'has_alt': bool(img.get('alt'))
            })
        
        # Extract links (for further crawling)
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(url, href)
            
            if self._is_same_domain(absolute_url):
                links.append(absolute_url)
        
        # Extract ARIA attributes
        aria_elements = []
        for element in soup.find_all(attrs={'aria-label': True}):
            aria_elements.append({
                'tag': element.name,
                'aria_label': element.get('aria-label')
            })
        
        return {
            'url': url,
            'title': title,
            'meta_description': meta_desc,
            'meta_tags': meta_tags,
            'h1_tags': h1_tags,
            'images': images,
            'links': list(set(links)),  # Deduplicate
            'aria_elements': aria_elements,
            'status_code': status_code,
            'html_snippet': html_content[:1000]  # First 1000 chars for context
        }
    
    def _is_same_domain(self, url: str) -> bool:
        """
        Check if URL belongs to the same domain (lenient with www)
        
        Normalizes domains by removing 'www.' prefix to allow:
        - example.com ↔ www.example.com
        - subdomain.example.com ↔ www.subdomain.example.com
        
        This ensures the crawler can follow links between www and non-www
        versions of the same domain without being blocked.
        """
        try:
            parsed = urlparse(url)
            url_domain = parsed.netloc.lower()
            base_domain = self.base_domain.lower()
            
            # Normalize by removing www. prefix from both domains
            url_domain_normalized = url_domain.removeprefix('www.')
            base_domain_normalized = base_domain.removeprefix('www.')
            
            return url_domain_normalized == base_domain_normalized
        except:
            return False


async def crawl_website(
    url: str,
    max_pages: int = 50,
    max_depth: int = 3
) -> List[Dict[str, Any]]:
    """
    Convenience function to crawl a website
    
    Args:
        url: Base URL to start crawling
        max_pages: Maximum number of pages to crawl
        max_depth: Maximum depth to crawl
    
    Returns:
        List of page data dictionaries
    """
    crawler = WebCrawler(
        base_url=url,
        max_pages=max_pages,
        max_depth=max_depth,
        timeout=settings.crawler_timeout
    )
    
    return await crawler.crawl()


# Example usage
if __name__ == "__main__":
    async def main():
        results = await crawl_website("https://example.com", max_pages=10, max_depth=2)
        print(f"Crawled {len(results)} pages")
        for page in results:
            print(f"- {page['url']}: {page['title']}")
    
    asyncio.run(main())

# Made with Bob
