"""
Standalone test script for alt text fix

Tests the fix_img_alt_text logic without requiring app dependencies.
Run from backend directory:
    python test_alt_text_fix_standalone.py
"""

import re

def fix_img_alt_text(html_snippet: str, alt_text: str = "Descriptive text about this image") -> str:
    """
    Fix missing or empty alt text in img tags
    
    This function:
    1. Replaces empty alt="" or alt='' with descriptive alt text
    2. Adds alt attribute if missing
    3. Does NOT create duplicate alt attributes
    4. Preserves all other attributes (src, class, width, height, etc.)
    
    Args:
        html_snippet: HTML string containing img tags
        alt_text: The alt text to use (default: "Descriptive text about this image")
    
    Returns:
        Fixed HTML with proper alt attributes
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


print("=" * 70)
print("Testing Alt Text Fix Helper Function")
print("=" * 70)

# Test cases
test_cases = [
    {
        "name": "Empty alt with double quotes",
        "input": '<img src="/hero-image.jpg" alt="">',
        "expected": '<img src="/hero-image.jpg" alt="Descriptive text about this image">',
    },
    {
        "name": "Empty alt with single quotes",
        "input": "<img src='/icon-services.png' alt=''>",
        "expected": '<img src=\'/icon-services.png\' alt="Descriptive text about this image">',
    },
    {
        "name": "Missing alt attribute",
        "input": '<img src="/photo-team.jpg">',
        "expected": '<img src="/photo-team.jpg" alt="Descriptive text about this image">',
    },
    {
        "name": "Missing alt with self-closing tag",
        "input": '<img src="/logo.png"/>',
        "expected": '<img src="/logo.png" alt="Descriptive text about this image"/>',
    },
    {
        "name": "Empty alt with other attributes",
        "input": '<img src="/hero.jpg" class="hero-image" width="800" alt="">',
        "expected": '<img src="/hero.jpg" class="hero-image" width="800" alt="Descriptive text about this image">',
    },
    {
        "name": "Multiple images with mixed issues",
        "input": '<img src="/hero-image.jpg" alt="">\n<img src="/icon-services.png">\n<img src="/photo-team.jpg" alt="">',
        "expected": '<img src="/hero-image.jpg" alt="Descriptive text about this image">\n<img src="/icon-services.png" alt="Descriptive text about this image">\n<img src="/photo-team.jpg" alt="Descriptive text about this image">',
    },
    {
        "name": "Existing non-empty alt (should replace)",
        "input": '<img src="/test.jpg" alt="old text">',
        "expected": '<img src="/test.jpg" alt="Descriptive text about this image">',
    },
]

print("\nRunning tests...\n")

passed = 0
failed = 0

for i, test in enumerate(test_cases, 1):
    result = fix_img_alt_text(test["input"])
    
    # Check for duplicate alt attributes
    img_count = test["input"].count('<img')
    alt_count = result.count('alt=')
    has_duplicate = alt_count > img_count
    
    if result == test["expected"] and not has_duplicate:
        print(f"✅ Test {i}: {test['name']}")
        print(f"   Input:    {test['input'][:60]}...")
        print(f"   Output:   {result[:60]}...")
        print(f"   Status:   PASS\n")
        passed += 1
    else:
        print(f"❌ Test {i}: {test['name']}")
        print(f"   Input:    {test['input']}")
        print(f"   Expected: {test['expected']}")
        print(f"   Got:      {result}")
        if has_duplicate:
            print(f"   ERROR:    Duplicate alt attributes detected! ({alt_count} alts for {img_count} images)")
        print(f"   Status:   FAIL\n")
        failed += 1

print("=" * 70)
print(f"Test Results: {passed} passed, {failed} failed")
print("=" * 70)

if failed == 0:
    print("\n✅ All tests passed! Alt text fix is working correctly.")
    print("\nThe fix ensures:")
    print("  1. ✅ Replaces empty alt=\"\" or alt='' with descriptive text")
    print("  2. ✅ Adds alt attribute when missing")
    print("  3. ✅ Does NOT create duplicate alt attributes")
    print("  4. ✅ Preserves other attributes (src, class, width, etc.)")
else:
    print(f"\n❌ {failed} test(s) failed. Please review the implementation.")

print("\n" + "=" * 70)
print("Testing with Real Seed Data Snippet")
print("=" * 70)

# Test with actual seed data snippet
seed_data_snippet = '<img src="/hero-image.jpg" alt="">\n<img src="/icon-services.png">\n<img src="/photo-team.jpg" alt="">'

print("\nBefore (from seed_data.py):")
print(seed_data_snippet)

fixed_snippet = fix_img_alt_text(seed_data_snippet)

print("\nAfter (recommendation):")
print(fixed_snippet)

# Verify no duplicates
duplicate_count = fixed_snippet.count('alt=')
img_count = fixed_snippet.count('<img')

print(f"\nVerification:")
print(f"  Images found: {img_count}")
print(f"  Alt attributes: {duplicate_count}")

if duplicate_count == img_count:
    print(f"  ✅ No duplicate alt attributes!")
else:
    print(f"  ❌ Duplicate alt attributes detected!")

print("\n" + "=" * 70)
print("Test Complete!")
print("=" * 70)

# Made with Bob
