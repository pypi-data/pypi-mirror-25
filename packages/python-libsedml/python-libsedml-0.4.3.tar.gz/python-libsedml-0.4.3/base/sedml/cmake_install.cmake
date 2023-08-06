# Install script for directory: /home/fbergmann/Development/libSEDML/sedml

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/sedml/common" TYPE FILE FILES
    "/home/fbergmann/Development/libSEDML/sedml/common/common.h"
    "/home/fbergmann/Development/libSEDML/sedml/common/extern.h"
    "/home/fbergmann/Development/libSEDML/sedml/common/libsedml-config.h"
    "/home/fbergmann/Development/libSEDML/sedml/common/operationReturnValues.h"
    "/home/fbergmann/Development/libSEDML/sedml/common/sedmlfwd.h"
    )
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/sedml" TYPE FILE FILES
    "/home/fbergmann/Development/libSEDML/sedml/SedAddXML.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedAlgorithm.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedAlgorithmParameter.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedBase.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedChange.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedChangeAttribute.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedChangeXML.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedComputeChange.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedConstructorException.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedCurve.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedDataDescription.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedDataGenerator.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedDataSet.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedDataSource.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedDocument.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedError.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedErrorLog.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedErrorTable.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedFunctionalRange.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedListOf.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedModel.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedNamespaces.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedOneStep.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedOutput.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedParameter.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedPlot2D.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedPlot3D.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedRange.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedReader.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedRemoveXML.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedRepeatedTask.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedReport.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedSetValue.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedSimulation.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedSlice.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedSteadyState.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedSubTask.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedSurface.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedTask.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedTypeCodes.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedTypes.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedUniformRange.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedUniformTimeCourse.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedVariable.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedVectorRange.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedVisitor.h"
    "/home/fbergmann/Development/libSEDML/sedml/SedWriter.h"
    )
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/sedml/common" TYPE FILE FILES
    "/home/fbergmann/Development/build_sedml/sedml/common/libsedml-version.h"
    "/home/fbergmann/Development/build_sedml/sedml/common/libsedml-config-common.h"
    "/home/fbergmann/Development/build_sedml/sedml/common/libsedml-namespace.h"
    "/home/fbergmann/Development/build_sedml/sedml/common/libsedml-package.h"
    )
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsedml.so.0.4.3"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsedml.so.0"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsedml.so"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      file(RPATH_CHECK
           FILE "${file}"
           RPATH "")
    endif()
  endforeach()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES
    "/home/fbergmann/Development/build_sedml/sedml/libsedml.so.0.4.3"
    "/home/fbergmann/Development/build_sedml/sedml/libsedml.so.0"
    "/home/fbergmann/Development/build_sedml/sedml/libsedml.so"
    )
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsedml.so.0.4.3"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsedml.so.0"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsedml.so"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      if(CMAKE_INSTALL_DO_STRIP)
        execute_process(COMMAND "/usr/bin/strip" "${file}")
      endif()
    endif()
  endforeach()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/sedml-config.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/sedml-config.cmake"
         "/home/fbergmann/Development/build_sedml/sedml/CMakeFiles/Export/lib/cmake/sedml-config.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/sedml-config-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/sedml-config.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake" TYPE FILE FILES "/home/fbergmann/Development/build_sedml/sedml/CMakeFiles/Export/lib/cmake/sedml-config.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake" TYPE FILE FILES "/home/fbergmann/Development/build_sedml/sedml/CMakeFiles/Export/lib/cmake/sedml-config-release.cmake")
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake" TYPE FILE FILES "/home/fbergmann/Development/build_sedml/sedml/sedml-config-version.cmake")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/fbergmann/Development/build_sedml/sedml/libsedml-static.a")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/sedml-static-config.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/sedml-static-config.cmake"
         "/home/fbergmann/Development/build_sedml/sedml/CMakeFiles/Export/lib/cmake/sedml-static-config.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/sedml-static-config-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/sedml-static-config.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake" TYPE FILE FILES "/home/fbergmann/Development/build_sedml/sedml/CMakeFiles/Export/lib/cmake/sedml-static-config.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake" TYPE FILE FILES "/home/fbergmann/Development/build_sedml/sedml/CMakeFiles/Export/lib/cmake/sedml-static-config-release.cmake")
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake" TYPE FILE FILES "/home/fbergmann/Development/build_sedml/sedml/sedml-static-config-version.cmake")
endif()

