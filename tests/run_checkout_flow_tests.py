#!/usr/bin/env python3
"""
Test runner for checkout to confirmation flow
Ensures tests run in the correct order:
1. Checkout page tests
2. Checkout to confirmation flow tests
3. Confirmation page tests
4. Slow network edge case tests
"""

import subprocess
import sys
import time
from pathlib import Path


def run_tests_in_order():
    """Run tests in the correct order for checkout to confirmation flow"""
    
    print("🚀 Starting Checkout to Confirmation Flow Tests")
    print("=" * 60)
    
    # Test files in order
    test_files = [
        "test_checkout.py",  # First: checkout page tests
        "test_checkout_to_confirmation_flow.py",  # Second: flow tests
        "test_confirmationpage.py",  # Third: confirmation page tests
        "test_slow_network_edge_cases.py",  # Fourth: slow network edge cases
    ]
    
    results = {}
    
    for test_file in test_files:
        if not Path(test_file).exists():
            print(f"⚠️  Warning: {test_file} not found, skipping...")
            continue
            
        print(f"\n📋 Running {test_file}...")
        print("-" * 40)
        
        start_time = time.time()
        
        try:
            # Run pytest for this specific file
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                test_file, 
                "-v", 
                "--tb=short",
                "--durations=10"
            ], capture_output=True, text=True, timeout=600)
            
            end_time = time.time()
            duration = end_time - start_time
            
            results[test_file] = {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "duration": duration
            }
            
            if result.returncode == 0:
                print(f"✅ {test_file} PASSED ({duration:.2f}s)")
            else:
                print(f"❌ {test_file} FAILED ({duration:.2f}s)")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {test_file} TIMED OUT")
            results[test_file] = {"returncode": -1, "timeout": True}
        except Exception as e:
            print(f"💥 {test_file} ERROR: {e}")
            results[test_file] = {"returncode": -1, "error": str(e)}
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r.get("returncode") == 0)
    failed_tests = total_tests - passed_tests
    
    print(f"Total test files: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    
    for test_file, result in results.items():
        status = "✅ PASS" if result.get("returncode") == 0 else "❌ FAIL"
        duration = result.get("duration", 0)
        print(f"{status} {test_file} ({duration:.2f}s)")
    
    if failed_tests > 0:
        print(f"\n❌ {failed_tests} test file(s) failed")
        sys.exit(1)
    else:
        print(f"\n🎉 All {total_tests} test file(s) passed!")
        sys.exit(0)


def run_specific_flow_tests():
    """Run only the flow-related tests"""
    
    print("🔄 Running Checkout to Confirmation Flow Tests Only")
    print("=" * 60)
    
    flow_tests = [
        "test_checkout_to_confirmation_flow.py",
        "test_slow_network_edge_cases.py"
    ]
    
    for test_file in flow_tests:
        if not Path(test_file).exists():
            print(f"⚠️  Warning: {test_file} not found, skipping...")
            continue
            
        print(f"\n📋 Running {test_file}...")
        
        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                test_file, 
                "-v", 
                "--tb=short"
            ], timeout=600)
            
            if result.returncode == 0:
                print(f"✅ {test_file} PASSED")
            else:
                print(f"❌ {test_file} FAILED")
                sys.exit(1)
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {test_file} TIMED OUT")
            sys.exit(1)
        except Exception as e:
            print(f"💥 {test_file} ERROR: {e}")
            sys.exit(1)
    
    print("\n🎉 All flow tests passed!")


def run_slow_network_tests():
    """Run only the slow network edge case tests"""
    
    print("🐌 Running Slow Network Edge Case Tests")
    print("=" * 60)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "test_slow_network_edge_cases.py", 
            "-v", 
            "--tb=short",
            "-k", "slow_network"
        ], timeout=600)
        
        if result.returncode == 0:
            print("✅ Slow network tests PASSED")
        else:
            print("❌ Slow network tests FAILED")
            sys.exit(1)
            
    except subprocess.TimeoutExpired:
        print("⏰ Slow network tests TIMED OUT")
        sys.exit(1)
    except Exception as e:
        print(f"💥 Slow network tests ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "flow":
            run_specific_flow_tests()
        elif sys.argv[1] == "slow":
            run_slow_network_tests()
        else:
            print("Usage: python run_checkout_flow_tests.py [flow|slow]")
            sys.exit(1)
    else:
        run_tests_in_order()
