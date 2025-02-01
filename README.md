**WebPulse**

WebPulse is a high-speed, multi-threaded domain status checker designed By @Mahhesshh to scan domains from an input file and categorize them based on HTTP status codes (200, 301, 403, 401, 404, 501). It saves the results in separate files within a specified folder and provides a real-time progress bar.

Features:

Multi-threaded scanning for faster performance.
Categorizes domains by HTTP status codes.
Automatically saves results in a user-specified folder.
Real-time progress tracking with a clean terminal display.
Optional features: HTTP headers display and response time measurement.

Prerequisites:

    Ensure you have Python 3.x installed.

    Install the required dependencies:

    pip install -r requirements.txt

Usage:

    python3 statuschecker.py input.txt -o output_folder

Arguments:

     input.txt: The file containing the list of domains to check.

     -o output_folder: The folder where the output files (output200.txt, output301.txt, etc.) will be saved.

Example

    python3 statuschecker.py domains.txt -o results

This will process domains.txt and save the results in the results folder.

Output Files

The tool generates separate files based on HTTP status codes:

     output200.txt - Domains returning 200 OK

     output301.txt - Domains returning 301 Moved Permanently

     output403.txt - Domains returning 403 Forbidden

     output401.txt - Domains returning 401 Unauthorized

    output404.txt - Domains returning 404 Not Found

    output501.txt - Domains returning 501 Not Implemented

Example Output

    Scanning 3/100 domains...
    Scanning 50/100 domains...
    Scanning 100/100 domains...

    Results saved in the 'results' folder.

License

This project is licensed under the MIT License.
