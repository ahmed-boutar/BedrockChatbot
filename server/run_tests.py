import subprocess
import sys
import os

def run_tests():
    """Run tests with coverage"""
    
    # Ensure we're in the server directory
    if not os.path.exists('tests'):
        print("Error: tests directory not found. Make sure you're in the server directory.")
        sys.exit(1)
    
    # Install test dependencies
    print("Installing test dependencies...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
    
    # Run tests with coverage
    print("\nRunning tests with coverage...")
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'tests/', 
            '--cov=.',
            '--cov-report=html',
            '--cov-report=term-missing',
            '--ignore=tests/',  # This excludes the tests directory from coverage
            '-v'
        ], check=True)
        
        print("\n✅ Tests completed successfully!")
        print("📊 Coverage report generated in htmlcov/index.html")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()