#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "sedml-static" for configuration "Release"
set_property(TARGET sedml-static APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(sedml-static PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "sbml-static;/home/fbergmann/Development/copasi-dependencies/bin/lib/libnuml-static.a"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libsedml-static.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS sedml-static )
list(APPEND _IMPORT_CHECK_FILES_FOR_sedml-static "${_IMPORT_PREFIX}/lib/libsedml-static.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
