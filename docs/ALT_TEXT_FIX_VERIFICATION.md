# Alt Text Fix Verification

## Problem Statement

The original mock recommendation logic for missing alt text had a bug that created duplicate `alt` attributes:

**Bad Output (Before Fix):**
```html
<img src="/hero-image.jpg" alt="" alt='Descriptive text about this image'>
```

**Expected Output (After Fix):**
```html
<img src="/hero-image.jpg" alt="Descriptive text about this image">
```

## Root Cause

The original implementation used simple string replacement:
```python
snippet.replace(">", " alt='Descriptive text about this image'>")
```

This approach:
- Added `alt` attribute before every `>` character
- Did not check if `alt` already existed
- Created duplicate attributes when `alt=""` was already present
- Violated HTML standards (duplicate attributes are invalid)

## Solution

Created a `fix_img_alt_text()` helper function in `src/backend/app/services/ai_service.py` that:

1. **Uses regex to properly parse img tags**
2. **Detects existing alt attributes** (empty or with value)
3. **Replaces existing alt values** instead of adding new ones
4. **Adds alt only when truly missing**
5. **Preserves all other attributes** (src, class, width, height, etc.)

### Implementation

```python
def fix_img_alt_text(html_snippet: str, alt_text: str = "Descriptive text about this image") -> str:
    """
    Fix missing or empty alt text in img tags
    
    This function:
    1. Replaces empty alt="" or alt='' with descriptive alt text
    2. Adds alt attribute if missing
    3. Does NOT create duplicate alt attributes
    4. Preserves all other attributes (src, class, width, height, etc.)
    """
    def fix_single_img(match):
        img_tag = match.group(0)
        
        # Check if alt attribute exists (empty or with value)
        if re.search(r'alt\s*=\s*["\'][^"\']*["\']', img_tag):
            # Replace existing alt attribute value
            fixed = re.sub(
                r'alt\s*=\s*["\'][^"\']*["\']',
                f'alt="{alt_text}"',
                img_tag
            )
            return fixed
        else:
            # Add alt attribute before closing > or />
            if img_tag.endswith('/>'):
                return img_tag[:-2] + f' alt="{alt_text}"/>'
            else:
                return img_tag[:-1] + f' alt="{alt_text}">'
    
    # Find all img tags and fix them
    fixed_html = re.sub(r'<img[^>]*/?>', fix_single_img, html_snippet)
    return fixed_html
```

### Usage in Mock Recommendations

```python
# In generate_mock_recommendation() function
if "alt" in description or "alt text" in title:
    # Use helper function to properly fix alt text without creating duplicates
    fixed_html = fix_img_alt_text(snippet) if snippet else "<img src='image.jpg' alt='Descriptive text about this image'>"
    
    return {
        "plain_language_explanation": "Images need alternative text...",
        "suggested_fix": fixed_html,  # Now uses fixed_html instead of snippet.replace()
        "confidence_score": 95.0,
        "reasoning": "Adding descriptive alt text meets WCAG 2.1..."
    }
```

## Test Results

All 7 test cases passed:

✅ **Test 1:** Empty alt with double quotes
- Input: `<img src="/hero-image.jpg" alt="">`
- Output: `<img src="/hero-image.jpg" alt="Descriptive text about this image">`

✅ **Test 2:** Empty alt with single quotes
- Input: `<img src='/icon-services.png' alt=''>`
- Output: `<img src='/icon-services.png' alt="Descriptive text about this image">`

✅ **Test 3:** Missing alt attribute
- Input: `<img src="/photo-team.jpg">`
- Output: `<img src="/photo-team.jpg" alt="Descriptive text about this image">`

✅ **Test 4:** Missing alt with self-closing tag
- Input: `<img src="/logo.png"/>`
- Output: `<img src="/logo.png" alt="Descriptive text about this image"/>`

✅ **Test 5:** Empty alt with other attributes
- Input: `<img src="/hero.jpg" class="hero-image" width="800" alt="">`
- Output: `<img src="/hero.jpg" class="hero-image" width="800" alt="Descriptive text about this image">`

✅ **Test 6:** Multiple images with mixed issues
- Input: 3 images with empty/missing alt
- Output: All 3 images have proper alt text, no duplicates

✅ **Test 7:** Existing non-empty alt (should replace)
- Input: `<img src="/test.jpg" alt="old text">`
- Output: `<img src="/test.jpg" alt="Descriptive text about this image">`

### Real Seed Data Test

**Before (from seed_data.py):**
```html
<img src="/hero-image.jpg" alt="">
<img src="/icon-services.png">
<img src="/photo-team.jpg" alt="">
```

**After (recommendation):**
```html
<img src="/hero-image.jpg" alt="Descriptive text about this image">
<img src="/icon-services.png" alt="Descriptive text about this image">
<img src="/photo-team.jpg" alt="Descriptive text about this image">
```

**Verification:**
- Images found: 3
- Alt attributes: 3
- ✅ No duplicate alt attributes!

## How to Test

### Run Standalone Test
```bash
cd src/backend
python test_alt_text_fix_standalone.py
```

### Test with Live API
```bash
# 1. Start the backend server
cd src/backend
uvicorn app.main:app --reload

# 2. Create a scan (in another terminal)
curl -X POST http://localhost:8000/api/v1/scans \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# 3. Get the scan_id from response, then get issues
curl http://localhost:8000/api/v1/scans/{scan_id}/issues

# 4. Find an issue with "alt" in title/description, get its issue_id

# 5. Request recommendation
curl http://localhost:8000/api/v1/recommendations/{issue_id} | jq .

# 6. Verify the suggested_fix field has NO duplicate alt attributes
```

### Expected API Response
```json
{
  "issue_id": "uuid-here",
  "plain_language_explanation": "Images need alternative text (alt text) to be accessible...",
  "suggested_fix": "<img src=\"/hero-image.jpg\" alt=\"Descriptive text about this image\">\n<img src=\"/icon-services.png\" alt=\"Descriptive text about this image\">\n<img src=\"/photo-team.jpg\" alt=\"Descriptive text about this image\">",
  "before_snippet": "<img src=\"/hero-image.jpg\" alt=\"\">\n<img src=\"/icon-services.png\">\n<img src=\"/photo-team.jpg\" alt=\"\">",
  "after_snippet": "<img src=\"/hero-image.jpg\" alt=\"Descriptive text about this image\">\n<img src=\"/icon-services.png\" alt=\"Descriptive text about this image\">\n<img src=\"/photo-team.jpg\" alt=\"Descriptive text about this image\">",
  "confidence_score": 95.0,
  "reasoning": "Adding descriptive alt text meets WCAG 2.1 Level A requirements..."
}
```

## Files Modified

1. **src/backend/app/services/ai_service.py**
   - Added `import re` for regex operations
   - Created `fix_img_alt_text()` helper function
   - Modified missing alt text recommendation to use the helper

2. **src/backend/test_alt_text_fix_standalone.py** (new)
   - Standalone test script with 7 test cases
   - Tests all edge cases (empty alt, missing alt, multiple images, etc.)
   - Verifies no duplicate attributes are created

3. **docs/ALT_TEXT_FIX_VERIFICATION.md** (this file)
   - Documents the problem, solution, and verification

## Impact on Demo

This fix ensures that when the demo shows:
1. ✅ User scans a website
2. ✅ System detects missing alt text issues
3. ✅ User clicks on an issue
4. ✅ AI generates a recommendation
5. ✅ **The suggested fix is valid HTML with no duplicate attributes**
6. ✅ Admin can copy/paste the fix directly into their code

### Before Fix (Demo Blocker)
```html
<!-- Invalid HTML - would break the demo -->
<img src="/hero-image.jpg" alt="" alt='Descriptive text about this image'>
```

### After Fix (Demo Ready)
```html
<!-- Valid HTML - ready for production -->
<img src="/hero-image.jpg" alt="Descriptive text about this image">
```

## Verification Checklist

- [x] Helper function created and tested
- [x] All 7 test cases pass
- [x] No duplicate alt attributes in any scenario
- [x] Preserves other attributes (src, class, width, etc.)
- [x] Works with empty alt="" and alt=''
- [x] Works with missing alt
- [x] Works with multiple images
- [x] Works with self-closing tags
- [x] Integrated into mock recommendation logic
- [x] Tested with real seed data snippet
- [x] Documentation created

## Next Steps

1. ✅ **Fix is complete and tested**
2. **Test with live API** (optional, requires backend running)
3. **Frontend integration** (when frontend team is ready)
4. **Demo rehearsal** (verify the fix shows correctly in UI)

## Summary

The alt text fix is **complete and verified**. The helper function properly handles all edge cases and ensures that recommendations generate valid HTML without duplicate attributes. This fix is critical for the demo because it shows that PublicPulse AI can generate production-ready fixes, not just identify problems.

---

**Made with IBM Bob** 🤖