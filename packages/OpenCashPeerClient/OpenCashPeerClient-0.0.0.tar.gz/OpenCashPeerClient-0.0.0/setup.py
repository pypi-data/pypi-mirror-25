from setuptools import setup, find_packages

setup(
    name="OpenCashPeerClient",
    version="0.0.0",
    packages=find_packages(),
    entry_points={"console_scripts":["opencash=openCashPeerClient.client:runProg"]},
    author="Aristeidis Tomaras",
    author_email="arisgold29@gmail.com",
    description="OpenCash client that connects to get peers",
    url="http://github.com/saavedra29/openCashPeerClient",
    include_package_data=True,
    data_files=[("", ["README.md" ,"LICENSE"])],
    license="MIT",
    zip_safe=False,
    classifiers=[]
)