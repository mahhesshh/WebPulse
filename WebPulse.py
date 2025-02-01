import requests
import argparse
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import threading

lock = threading.Lock()

ascii_art = r"""


░  ░░░░  ░░        ░░       ░░░       ░░░  ░░░░  ░░  ░░░░░░░░░      ░░░        ░
▒  ▒  ▒  ▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒
▓        ▓▓      ▓▓▓▓       ▓▓▓       ▓▓▓  ▓▓▓▓  ▓▓  ▓▓▓▓▓▓▓▓▓      ▓▓▓      ▓▓▓
█   ██   ██  ████████  ████  ██  ████████  ████  ██  ██████████████  ██  ███████
█  ████  ██        ██       ███  █████████      ███        ███      ███        █
                                                                                
                                    Created By @mahhesshh by ❤︎
                                            
"""

print(ascii_art)


def check_domain(domain, status_codes, output_files, summary):
    if not domain.startswith(('http://', 'https://')):
        domain = 'http://' + domain  # Default to HTTP if no scheme
    
    try:
        response = requests.get(domain, timeout=5)
        code = response.status_code
        
        with lock:
            if code in status_codes:
                output_files[code].write(f"{domain}\n")
                summary[code] += 1
            else:
                output_files[404].write(f"{domain}\n")
                summary[404] += 1
    except requests.exceptions.RequestException:
        with lock:
            output_files[404].write(f"{domain}\n")
            summary[404] += 1


def check_domains(input_file, output_prefix, threads):
    status_codes = [200, 301, 401, 403, 404, 501]
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_prefix):
        os.makedirs(output_prefix)
    
    # Prepare output files inside the folder
    output_files = {code: open(os.path.join(output_prefix, f"{code}.txt"), "w") for code in status_codes}
    summary = {code: 0 for code in status_codes}
    
    with open(input_file, 'r') as infile:
        domains = [line.strip() for line in infile if line.strip()]
    
    total_domains = len(domains)

    # Using tqdm for progress bar
    with ThreadPoolExecutor(max_workers=threads) as executor, tqdm(total=total_domains, desc="Scanning Domains", unit="domain") as pbar:
        futures = [executor.submit(check_domain, domain, status_codes, output_files, summary) for domain in domains]
        
        for future in as_completed(futures):
            pbar.update(1)
    
    for file in output_files.values():
        file.close()

    # Generate Summary Report
    print("\n\nSummary Report:")
    print(f"Total Domains Scanned: {total_domains}")
    for code in status_codes:
        print(f"{code}: {summary[code]}")

    # Save Summary Report inside the output folder
    summary_path = os.path.join(output_prefix, "summary.txt")
    with open(summary_path, "w") as summary_file:
        summary_file.write(f"Total Domains Scanned: {total_domains}\n")
        for code in status_codes:
            summary_file.write(f"{code}: {summary[code]}\n")

    print(f"\nSummary saved to {summary_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check HTTP status codes for domains.")
    
    parser.add_argument("input_file", help="Path to the input file containing domains.")
    parser.add_argument("-o", "--output_prefix", required=True, help="Folder name for the output files.")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Number of threads to use (default: 20).")
    
    args = parser.parse_args()
    
    check_domains(args.input_file, args.output_prefix, args.threads)
