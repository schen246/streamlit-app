# Binary Search
# Description: Given a sorted array of integers nums and a target value, return the index of target in nums. If target is not found, return -1.

Example 1:
Input: nums = [-1, 0, 3, 5, 9, 12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4

Example 2:
Input: nums = [-1, 0, 3, 5, 9, 12], target = 2
Output: -1
Explanation: 2 does not exist in nums so return -1

Constraints:
- nums is sorted in ascending order
- All values in nums are unique
- 1 <= nums.length <= 10^4
- -10^4 <= nums[i], target <= 10^4

def binary_search(nums: list[int], target: int) -> int:
    # Write your binary search implementation here
    left = 0
    right = len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1