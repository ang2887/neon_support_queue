# setup.py

from setuptools import setup, find_packages

setup(
    name="neon_support_queue_classic",
    version="0.1.0",
    description="Visualize and monitor customer support ticket wait times, with alerts for Neon DB usage thresholds.",
    author="Lena Docherty",
    author_email="ang2887@gmail.com",
    packages=find_packages(),  # Automatically find all packages in the project
    include_package_data=True,
    install_requires=[
        # Core dependencies 
        "pandas",
        "dash",
        "plotly",
        "schedule",
        "python-dotenv"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)