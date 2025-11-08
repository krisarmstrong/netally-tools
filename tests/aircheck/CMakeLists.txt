if (NOT TARGET GTest::gtest_main)
  message(FATAL_ERROR "GoogleTest dependency not found. Ensure FetchContent_MakeAvailable(googletest) was called.")
endif()

add_executable(aircheck_tests
  aircheck_tests.cpp
  integration_tests.cpp
)

target_link_libraries(aircheck_tests
  PRIVATE
    GTest::gtest_main
)

include(GoogleTest)
gtest_discover_tests(aircheck_tests)
