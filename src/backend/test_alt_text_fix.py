"""
Test script for alt text recommendation fix

This verifies that the fix_img_alt_text helper function:
1. Replaces empty alt="" or alt='' with descriptive text
2. Adds alt attribute when missing
3. Does NOT create duplicate alt attributes
4. Preserves other attributes

Run from backend directory:
    python test_alt_text_fix.py
"""

from app.services.ai_service import fix_img_alt_text

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
    has_duplicate = result.count('alt=') > test["input"].count('<img')
    
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
            print(f"   ERROR:    Duplicate alt attributes detected!")
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