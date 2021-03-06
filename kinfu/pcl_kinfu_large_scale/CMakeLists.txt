set(CUDA_USE_STATIC_CUDA_RUNTIME OFF)
find_package(CUDA REQUIRED)
message(STATUS "kinfu: CUDA ${CUDA_VERSION} found.")

include(${CMAKE_CURRENT_SOURCE_DIR}/remove_vtk_definitions_hack.cmake)
REMOVE_VTK_DEFINITIONS()

set(KinfuLargeScale_INCLUDE_DIRS
  ${CMAKE_CURRENT_SOURCE_DIR}/containers/include
  ${CMAKE_CURRENT_SOURCE_DIR}/utils/include
  ${CMAKE_CURRENT_SOURCE_DIR}/kinfu_large_scale/include
  ${CMAKE_CURRENT_SOURCE_DIR}/kinfu_large_scale/src
  )

set(KinfuLargeScale_INCLUDE_DIRS
  ${KinfuLargeScale_INCLUDE_DIRS}
  ${CUDA_INCLUDE_DIRS}
  PARENT_SCOPE
  )

include_directories(
  ${KinfuLargeScale_INCLUDE_DIRS}
  )

include_directories(
  ${PCL_INCLUDE_DIRS}
  ${CUDA_INCLUDE_DIRS}
  )

link_directories(${PCL_LIBRARY_DIRS})

add_library(
  KinfuLargeScaleCPP
  SHARED
  containers/src/device_memory.cpp
  containers/src/error.cpp
  containers/src/initialization.cpp

  kinfu_large_scale/src/color_volume.cpp
  kinfu_large_scale/src/cyclical_buffer.cpp
  kinfu_large_scale/src/kinfu.cpp
  kinfu_large_scale/src/marching_cubes.cpp
  kinfu_large_scale/src/raycaster.cpp
  kinfu_large_scale/src/screenshot_manager.cpp
  kinfu_large_scale/src/standalone_marching_cubes.cpp
  kinfu_large_scale/src/tsdf_volume.cpp
  kinfu_large_scale/src/world_model.cpp
  )

target_link_libraries(
  KinfuLargeScaleCPP ${PCL_LIBRARIES}
)

set(CUDA_NVCC_FLAGS "-gencode arch=compute_20,code=sm_20 -gencode arch=compute_30,code=sm_30 -gencode arch=compute_35,code=sm_35 -gencode arch=compute_50,code=sm_50 -gencode arch=compute_52,code=sm_52")
set(CUDA_NVCC_FLAGS ${CUDA_NVCC_FLAGS} "--ftz=true --prec-div=false --prec-sqrt=false")	
set(CUDA_VERBOSE_BUILD OFF)
cuda_add_library(KinfuLargeScaleCUDA
  SHARED 
  kinfu_large_scale/src/cuda/bilateral_pyrdown.cu
  kinfu_large_scale/src/cuda/colors.cu
  kinfu_large_scale/src/cuda/coresp.cu
  kinfu_large_scale/src/cuda/estimate_combined.cu
  kinfu_large_scale/src/cuda/estimate_tranform.cu
  kinfu_large_scale/src/cuda/extract.cu
  kinfu_large_scale/src/cuda/image_generator.cu
  kinfu_large_scale/src/cuda/maps.cu
  kinfu_large_scale/src/cuda/marching_cubes.cu
  kinfu_large_scale/src/cuda/normals_eigen.cu
  kinfu_large_scale/src/cuda/pointer_shift.cu
  kinfu_large_scale/src/cuda/push.cu
  kinfu_large_scale/src/cuda/ray_caster.cu
  kinfu_large_scale/src/cuda/tsdf_volume.cu
)

target_link_libraries(
  KinfuLargeScaleCUDA
  ${PCL_LIBRARIES}
)

set(KinfuLargeScale_LIBRARIES KinfuLargeScaleCPP KinfuLargeScaleCUDA PARENT_SCOPE)

# installation
# added by tongxi lou(lou@magazino.eu)
# currently install to CATKIN_WS/lib, otherwise not recognised
install(TARGETS KinfuLargeScaleCPP KinfuLargeScaleCUDA
  ARCHIVE DESTINATION lib#/pcl_kinfu_large_scale#${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION lib#/pcl_kinfu_large_scale#${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION bin#/pcl_kinfu_large_scale#${CATKIN_PACKAGE_BIN_DESTINATION}
)
## CAUTION: installing pcl from source may lead to ignorance of this subdirectory, so remove or disable
## pcl::gpu on computer first
