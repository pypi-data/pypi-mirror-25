#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "sedml" for configuration "Release"
set_property(TARGET sedml APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(sedml PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "sbml-static;/home/fbergmann/Development/copasi-dependencies/bin/lib/libnuml-static.a"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libsedml.so.0.4.3"
  IMPORTED_SONAME_RELEASE "libsedml.so.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS sedml )
list(APPEND _IMPORT_CHECK_FILES_FOR_sedml "${_IMPORT_PREFIX}/lib/libsedml.so.0.4.3" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
