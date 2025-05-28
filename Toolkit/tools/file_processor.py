#!/usr/bin/env python3
"""
File Batch Processor Tool
Processes multiple files with various operations
"""

import json
import sys
import os
import glob
import shutil
from pathlib import Path

def process_files(inputs):
    """Main file processing logic"""
    source_folder = inputs['source_folder']
    output_folder = inputs['output_folder']
    operation = inputs['operation'].lower()
    pattern = inputs['pattern']
    recursive = inputs['recursive']
    
    print(f"🔍 Scanning for files: {pattern}")
    print(f"📁 Source: {source_folder}")
    print(f"📁 Output: {output_folder}")
    print(f"🔄 Operation: {operation}")
    print(f"📂 Recursive: {'Yes' if recursive else 'No'}")
    print("-" * 50)
    
    # Validate source folder
    if not os.path.exists(source_folder):
        print(f"❌ Source folder doesn't exist: {source_folder}")
        return 1
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Build file search pattern
    if recursive:
        search_pattern = os.path.join(source_folder, "**", pattern)
        files = glob.glob(search_pattern, recursive=True)
    else:
        search_pattern = os.path.join(source_folder, pattern)
        files = glob.glob(search_pattern)
    
    if not files:
        print(f"⚠️  No files found matching pattern: {pattern}")
        return 0
    
    print(f"📊 Found {len(files)} files to process")
    
    processed_count = 0
    error_count = 0
    
    for file_path in files:
        try:
            filename = os.path.basename(file_path)
            print(f"🔧 Processing: {filename}")
            
            if operation == 'rename':
                # Example: add timestamp prefix
                timestamp = "processed_"
                new_name = timestamp + filename
                output_path = os.path.join(output_folder, new_name)
                shutil.copy2(file_path, output_path)
                
            elif operation == 'convert':
                # Example: convert text to uppercase (for .txt files)
                if file_path.endswith('.txt'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().upper()
                    output_path = os.path.join(output_folder, filename)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                else:
                    # Just copy if not a text file
                    output_path = os.path.join(output_folder, filename)
                    shutil.copy2(file_path, output_path)
                    
            elif operation == 'compress':
                # Example: create a compressed copy (this would need actual compression)
                output_path = os.path.join(output_folder, filename)
                shutil.copy2(file_path, output_path)
                print(f"   📦 (Compression logic would go here)")
                
            elif operation == 'organize':
                # Example: organize by file extension
                file_ext = Path(file_path).suffix.lower()
                if file_ext:
                    ext_folder = os.path.join(output_folder, file_ext[1:])  # Remove the dot
                    os.makedirs(ext_folder, exist_ok=True)
                    output_path = os.path.join(ext_folder, filename)
                else:
                    output_path = os.path.join(output_folder, "no_extension", filename)
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                shutil.copy2(file_path, output_path)
                
            else:
                print(f"   ⚠️  Unknown operation: {operation}")
                continue
                
            processed_count += 1
            print(f"   ✅ Done")
            
        except Exception as e:
            error_count += 1
            print(f"   ❌ Error: {str(e)}")
    
    print("-" * 50)
    print(f"📊 Processing Summary:")
    print(f"   ✅ Successfully processed: {processed_count} files")
    if error_count > 0:
        print(f"   ❌ Errors encountered: {error_count} files")
    print(f"   📁 Output location: {output_folder}")
    
    return 0

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("❌ No input provided")
        return 1
    
    try:
        inputs = json.loads(sys.argv[1])
        return process_files(inputs)
    except json.JSONDecodeError:
        print("❌ Invalid input format")
        return 1
    except Exception as e:
        print(f"💥 Unexpected error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
