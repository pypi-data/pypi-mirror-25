typedef struct VmaAllocator_T *VmaAllocator;

typedef void (*PFN_vmaAllocateDeviceMemoryFunction)(
    VmaAllocator      allocator,
    uint32_t          memoryType,
    VkDeviceMemory    memory,
    VkDeviceSize      size);
typedef void (*PFN_vmaFreeDeviceMemoryFunction)(
    VmaAllocator      allocator,
    uint32_t          memoryType,
    VkDeviceMemory    memory,
    VkDeviceSize      size);

typedef struct VmaDeviceMemoryCallbacks {
    PFN_vmaAllocateDeviceMemoryFunction pfnAllocate;
    PFN_vmaFreeDeviceMemoryFunction pfnFree;
} VmaDeviceMemoryCallbacks;

typedef enum VmaAllocatorFlagBits {
    VMA_ALLOCATOR_EXTERNALLY_SYNCHRONIZED_BIT = 0x00000001,

    VMA_ALLOCATOR_FLAG_BITS_MAX_ENUM = 0x7FFFFFFF
} VmaAllocatorFlagBits;
typedef VkFlags VmaAllocatorFlags;

typedef struct VmaVulkanFunctions {
    PFN_vkGetPhysicalDeviceProperties vkGetPhysicalDeviceProperties;
    PFN_vkGetPhysicalDeviceMemoryProperties vkGetPhysicalDeviceMemoryProperties;
    PFN_vkAllocateMemory vkAllocateMemory;
    PFN_vkFreeMemory vkFreeMemory;
    PFN_vkMapMemory vkMapMemory;
    PFN_vkUnmapMemory vkUnmapMemory;
    PFN_vkBindBufferMemory vkBindBufferMemory;
    PFN_vkBindImageMemory vkBindImageMemory;
    PFN_vkGetBufferMemoryRequirements vkGetBufferMemoryRequirements;
    PFN_vkGetImageMemoryRequirements vkGetImageMemoryRequirements;
    PFN_vkCreateBuffer vkCreateBuffer;
    PFN_vkDestroyBuffer vkDestroyBuffer;
    PFN_vkCreateImage vkCreateImage;
    PFN_vkDestroyImage vkDestroyImage;
} VmaVulkanFunctions;

typedef struct VmaAllocatorCreateInfo
{
    VmaAllocatorFlags flags;
    VkPhysicalDevice physicalDevice;
    VkDevice device;
    VkDeviceSize preferredLargeHeapBlockSize;
    VkDeviceSize preferredSmallHeapBlockSize;
    const VkAllocationCallbacks* pAllocationCallbacks;
    const VmaDeviceMemoryCallbacks* pDeviceMemoryCallbacks;
    uint32_t frameInUseCount;
    const VkDeviceSize* pHeapSizeLimit;
    const VmaVulkanFunctions* pVulkanFunctions;
} VmaAllocatorCreateInfo;

VkResult vmaCreateAllocator(
    const VmaAllocatorCreateInfo* pCreateInfo,
    VmaAllocator* pAllocator);

void vmaDestroyAllocator(
    VmaAllocator allocator);

void vmaGetPhysicalDeviceProperties(
    VmaAllocator allocator,
    const VkPhysicalDeviceProperties** ppPhysicalDeviceProperties);

void vmaGetMemoryProperties(
    VmaAllocator allocator,
    const VkPhysicalDeviceMemoryProperties** ppPhysicalDeviceMemoryProperties);

void vmaGetMemoryTypeProperties(
    VmaAllocator allocator,
    uint32_t memoryTypeIndex,
    VkMemoryPropertyFlags* pFlags);

void vmaSetCurrentFrameIndex(
    VmaAllocator allocator,
    uint32_t frameIndex);

typedef struct VmaStatInfo
{
    uint32_t blockCount;
    uint32_t allocationCount;
    uint32_t unusedRangeCount;
    VkDeviceSize usedBytes;
    VkDeviceSize unusedBytes;
    VkDeviceSize allocationSizeMin, allocationSizeAvg, allocationSizeMax;
    VkDeviceSize unusedRangeSizeMin, unusedRangeSizeAvg, unusedRangeSizeMax;
} VmaStatInfo;

typedef struct VmaStats
{
    VmaStatInfo memoryType[32];
    VmaStatInfo memoryHeap[16];
    VmaStatInfo total;
} VmaStats;

void vmaCalculateStats(
    VmaAllocator allocator,
    VmaStats* pStats);

void vmaBuildStatsString(
    VmaAllocator allocator,
    char** ppStatsString,
    VkBool32 detailedMap);

void vmaFreeStatsString(
    VmaAllocator allocator,
    char* pStatsString);

typedef struct VmaPool_T *VmaPool;

typedef enum VmaMemoryUsage
{
    VMA_MEMORY_USAGE_UNKNOWN = 0,
    VMA_MEMORY_USAGE_GPU_ONLY = 1,
    VMA_MEMORY_USAGE_CPU_ONLY = 2,
    VMA_MEMORY_USAGE_CPU_TO_GPU = 3,
    VMA_MEMORY_USAGE_GPU_TO_CPU = 4,
    VMA_MEMORY_USAGE_MAX_ENUM = 0x7FFFFFFF
} VmaMemoryUsage;

typedef enum VmaAllocationCreateFlagBits {
    VMA_ALLOCATION_CREATE_OWN_MEMORY_BIT = 0x00000001,
    VMA_ALLOCATION_CREATE_NEVER_ALLOCATE_BIT = 0x00000002,
    VMA_ALLOCATION_CREATE_PERSISTENT_MAP_BIT = 0x00000004,
    VMA_ALLOCATION_CREATE_CAN_BECOME_LOST_BIT = 0x00000008,
    VMA_ALLOCATION_CREATE_CAN_MAKE_OTHER_LOST_BIT = 0x00000010,
    VMA_ALLOCATION_CREATE_FLAG_BITS_MAX_ENUM = 0x7FFFFFFF
} VmaAllocationCreateFlagBits;
typedef VkFlags VmaAllocationCreateFlags;

typedef struct VmaAllocationCreateInfo
{
    VmaAllocationCreateFlags flags;
    VmaMemoryUsage usage;
    VkMemoryPropertyFlags requiredFlags;
    VkMemoryPropertyFlags preferredFlags;
    void* pUserData;
    VmaPool pool;
} VmaAllocationCreateInfo;

VkResult vmaFindMemoryTypeIndex(
    VmaAllocator allocator,
    uint32_t memoryTypeBits,
    const VmaAllocationCreateInfo* pAllocationCreateInfo,
    uint32_t* pMemoryTypeIndex);

typedef enum VmaPoolCreateFlagBits {
    VMA_POOL_CREATE_PERSISTENT_MAP_BIT = 0x00000001,
    VMA_POOL_CREATE_IGNORE_BUFFER_IMAGE_GRANULARITY_BIT = 0x00000002,
    VMA_POOL_CREATE_FLAG_BITS_MAX_ENUM = 0x7FFFFFFF
} VmaPoolCreateFlagBits;
typedef VkFlags VmaPoolCreateFlags;

typedef struct VmaPoolCreateInfo {
    uint32_t memoryTypeIndex;
    VmaPoolCreateFlags flags;
    VkDeviceSize blockSize;
    size_t minBlockCount;
    size_t maxBlockCount;
    uint32_t frameInUseCount;
} VmaPoolCreateInfo;

typedef struct VmaPoolStats {
    VkDeviceSize size;
    VkDeviceSize unusedSize;
    size_t allocationCount;
    size_t unusedRangeCount;
    VkDeviceSize unusedRangeSizeMax;
} VmaPoolStats;

VkResult vmaCreatePool(
	VmaAllocator allocator,
	const VmaPoolCreateInfo* pCreateInfo,
	VmaPool* pPool);

void vmaDestroyPool(
    VmaAllocator allocator,
    VmaPool pool);

void vmaGetPoolStats(
    VmaAllocator allocator,
    VmaPool pool,
    VmaPoolStats* pPoolStats);

void vmaMakePoolAllocationsLost(
    VmaAllocator allocator,
    VmaPool pool,
    size_t* pLostAllocationCount);

typedef struct VmaAllocation_T *VmaAllocation;

typedef struct VmaAllocationInfo {
    uint32_t memoryType;
    VkDeviceMemory deviceMemory;
    VkDeviceSize offset;
    VkDeviceSize size;
    void* pMappedData;
    void* pUserData;
} VmaAllocationInfo;

VkResult vmaAllocateMemory(
    VmaAllocator allocator,
    const VkMemoryRequirements* pVkMemoryRequirements,
    const VmaAllocationCreateInfo* pCreateInfo,
    VmaAllocation* pAllocation,
    VmaAllocationInfo* pAllocationInfo);

VkResult vmaAllocateMemoryForBuffer(
    VmaAllocator allocator,
    VkBuffer buffer,
    const VmaAllocationCreateInfo* pCreateInfo,
    VmaAllocation* pAllocation,
    VmaAllocationInfo* pAllocationInfo);

VkResult vmaAllocateMemoryForImage(
    VmaAllocator allocator,
    VkImage image,
    const VmaAllocationCreateInfo* pCreateInfo,
    VmaAllocation* pAllocation,
    VmaAllocationInfo* pAllocationInfo);

void vmaFreeMemory(
    VmaAllocator allocator,
    VmaAllocation allocation);

void vmaGetAllocationInfo(
    VmaAllocator allocator,
    VmaAllocation allocation,
    VmaAllocationInfo* pAllocationInfo);

void vmaSetAllocationUserData(
    VmaAllocator allocator,
    VmaAllocation allocation,
    void* pUserData);

void vmaCreateLostAllocation(
    VmaAllocator allocator,
    VmaAllocation* pAllocation);

VkResult vmaMapMemory(
    VmaAllocator allocator,
    VmaAllocation allocation,
    void** ppData);

void vmaUnmapMemory(
    VmaAllocator allocator,
    VmaAllocation allocation);

void vmaUnmapPersistentlyMappedMemory(VmaAllocator allocator);

VkResult vmaMapPersistentlyMappedMemory(VmaAllocator allocator);

typedef struct VmaDefragmentationInfo {
    VkDeviceSize maxBytesToMove;
    uint32_t maxAllocationsToMove;
} VmaDefragmentationInfo;

typedef struct VmaDefragmentationStats {
    VkDeviceSize bytesMoved;
    VkDeviceSize bytesFreed;
    uint32_t allocationsMoved;
    uint32_t deviceMemoryBlocksFreed;
} VmaDefragmentationStats;

VkResult vmaDefragment(
    VmaAllocator allocator,
    VmaAllocation* pAllocations,
    size_t allocationCount,
    VkBool32* pAllocationsChanged,
    const VmaDefragmentationInfo *pDefragmentationInfo,
    VmaDefragmentationStats* pDefragmentationStats);

VkResult vmaCreateBuffer(
    VmaAllocator allocator,
    const VkBufferCreateInfo* pBufferCreateInfo,
    const VmaAllocationCreateInfo* pAllocationCreateInfo,
    VkBuffer* pBuffer,
    VmaAllocation* pAllocation,
    VmaAllocationInfo* pAllocationInfo);

void vmaDestroyBuffer(
    VmaAllocator allocator,
    VkBuffer buffer,
    VmaAllocation allocation);

VkResult vmaCreateImage(
    VmaAllocator allocator,
    const VkImageCreateInfo* pImageCreateInfo,
    const VmaAllocationCreateInfo* pAllocationCreateInfo,
    VkImage* pImage,
    VmaAllocation* pAllocation,
    VmaAllocationInfo* pAllocationInfo);

void vmaDestroyImage(
    VmaAllocator allocator,
    VkImage image,
    VmaAllocation allocation);
