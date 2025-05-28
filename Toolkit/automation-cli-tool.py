#!/usr/bin/env python3
"""
Personal Automation Toolkit - Terminal Edition
A simple CLI interface for all your automation scripts
"""

import os
import sys
import subprocess
import json
from datetime import datetime
import time

class AutomationToolkit:
    def __init__(self):
        self.tools = {
            1: {
                'name': 'File Batch Processor',
                'description': 'Process multiple files with custom operations',
                'script': 'file_processor.py',
                'inputs': [
                    {'name': 'source_folder', 'prompt': 'Enter source folder path: ', 'type': 'str'},
                    {'name': 'output_folder', 'prompt': 'Enter output folder path: ', 'type': 'str'},
                    {'name': 'operation', 'prompt': 'Operation (rename/convert/compress): ', 'type': 'str'},
                    {'name': 'pattern', 'prompt': 'File pattern (e.g., *.txt): ', 'type': 'str'},
                    {'name': 'recursive', 'prompt': 'Include subfolders? (y/n): ', 'type': 'bool'}
                ]
            },
            2: {
                'name': 'Data Report Generator',
                'description': 'Generate reports from CSV/Excel data',
                'script': 'data_analyzer.py',
                'inputs': [
                    {'name': 'data_file', 'prompt': 'Enter data file path: ', 'type': 'str'},
                    {'name': 'report_type', 'prompt': 'Report type (summary/detailed/trends): ', 'type': 'str'},
                    {'name': 'output_format', 'prompt': 'Output format (PDF/Excel/HTML): ', 'type': 'str'},
                    {'name': 'include_charts', 'prompt': 'Include charts? (y/n): ', 'type': 'bool'}
                ]
            },
            3: {
                'name': 'Email Campaign Manager',
                'description': 'Send automated emails with templates',
                'script': 'email_automation.py',
                'inputs': [
                    {'name': 'recipient_list', 'prompt': 'Recipients CSV file path: ', 'type': 'str'},
                    {'name': 'template', 'prompt': 'Template (welcome/followup/newsletter): ', 'type': 'str'},
                    {'name': 'subject', 'prompt': 'Email subject: ', 'type': 'str'},
                    {'name': 'test_mode', 'prompt': 'Test mode only? (y/n): ', 'type': 'bool'}
                ]
            },
            4: {
                'name': 'System Monitor',
                'description': 'Monitor system resources and generate alerts',
                'script': 'system_monitor.py',
                'inputs': [
                    {'name': 'check_type', 'prompt': 'Check (cpu/memory/disk/all): ', 'type': 'str'},
                    {'name': 'threshold', 'prompt': 'Alert threshold (%): ', 'type': 'int'},
                    {'name': 'duration', 'prompt': 'Monitor duration (minutes): ', 'type': 'int'}
                ]
            },
            5: {
                'name': 'Database Backup',
                'description': 'Backup databases with compression',
                'script': 'db_backup.py',
                'inputs': [
                    {'name': 'db_type', 'prompt': 'Database type (mysql/postgres/sqlite): ', 'type': 'str'},
                    {'name': 'db_name', 'prompt': 'Database name: ', 'type': 'str'},
                    {'name': 'backup_location', 'prompt': 'Backup location: ', 'type': 'str'},
                    {'name': 'compress', 'prompt': 'Compress backup? (y/n): ', 'type': 'bool'}
                ]
            }
        }
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
    def print_banner(self):
        banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║      ██████╗ ██╗   ██╗████████╗ ██████╗ ███╗   ███╗ █████╗ ████████╗███████╗ ║
║     ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗████╗ ████║██╔══██╗╚══██╔══╝██╔════╝ ║
║     ██████╔╝██║   ██║   ██║   ██║   ██║██╔████╔██║███████║   ██║   █████╗   ║
║     ██╔══██╗██║   ██║   ██║   ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══╝   ║
║     ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║ ╚═╝ ██║██║  ██║   ██║   ███████╗ ║
║     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝ ║
║                                                                               ║
║                     🔧 Personal Automation Toolkit 🔧                        ║
║                        Your Scripts, Simplified                              ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
        
    def print_menu(self):
        print("\n" + "="*80)
        print(" 🛠️  AVAILABLE AUTOMATION TOOLS")
        print("="*80)
        
        for num, tool in self.tools.items():
            print(f" [{num}] {tool['name']}")
            print(f"     └─ {tool['description']}")
            print()
            
        print(" [0] Exit")
        print("="*80)
        
    def get_user_input(self, input_config):
        """Get and validate user input based on type"""
        while True:
            try:
                value = input(f" {input_config['prompt']}")
                
                if input_config['type'] == 'bool':
                    return value.lower() in ['y', 'yes', 'true', '1']
                elif input_config['type'] == 'int':
                    return int(value)
                elif input_config['type'] == 'float':
                    return float(value)
                else:  # str
                    return value
                    
            except ValueError:
                print(f" ❌ Invalid input. Please enter a valid {input_config['type']}.")
                
    def collect_inputs(self, tool):
        """Collect all inputs for a tool"""
        print(f"\n🔧 Configuring: {tool['name']}")
        print("-" * 60)
        
        inputs = {}
        for input_config in tool['inputs']:
            inputs[input_config['name']] = self.get_user_input(input_config)
            
        return inputs
        
    def run_tool(self, tool, inputs):
        """Execute the tool with given inputs"""
        script_path = os.path.join('tools', tool['script'])
        
        # Check if script exists
        if not os.path.exists(script_path):
            print(f"\n⚠️  Script not found: {script_path}")
            print("   Creating placeholder script...")
            self.create_placeholder_script(script_path, tool, inputs)
            return
            
        print(f"\n🚀 Executing: {tool['name']}")
        print("-" * 60)
        
        try:
            # Convert inputs to JSON for passing to script
            inputs_json = json.dumps(inputs)
            
            # Run the script
            start_time = time.time()
            result = subprocess.run(
                [sys.executable, script_path, inputs_json],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                print(f"✅ Success! Completed in {execution_time:.2f} seconds")
                if result.stdout:
                    print(f"📄 Output:\n{result.stdout}")
            else:
                print(f"❌ Error (Exit code: {result.returncode})")
                if result.stderr:
                    print(f"🔍 Error details:\n{result.stderr}")
                    
        except subprocess.TimeoutExpired:
            print("⏰ Script execution timed out (5 minutes)")
        except Exception as e:
            print(f"💥 Execution failed: {str(e)}")
            
    def create_placeholder_script(self, script_path, tool, inputs):
        """Create a placeholder script if it doesn't exist"""
        os.makedirs('tools', exist_ok=True)
        
        placeholder_content = f'''#!/usr/bin/env python3
"""
{tool['name']} - Automation Script
Generated placeholder - Replace with your actual implementation
"""

import json
import sys

def main():
    if len(sys.argv) > 1:
        inputs = json.loads(sys.argv[1])
        print(f"Received inputs: {{inputs}}")
    
    # TODO: Replace this with your actual automation logic
    print("🔨 This is a placeholder script for: {tool['name']}")
    print("📝 Description: {tool['description']}")
    print("⚡ Add your automation logic here!")
    
    # Example of using inputs:
    for key, value in inputs.items():
        print(f"   {key}: {value}")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
'''
        
        with open(script_path, 'w') as f:
            f.write(placeholder_content)
            
        os.chmod(script_path, 0o755)  # Make executable
        print(f"📝 Created placeholder: {script_path}")
        print("   Edit this file to add your automation logic!")
        
    def run_selected_tool(self, choice):
        """Run the selected tool"""
        if choice not in self.tools:
            print("\n❌ Invalid selection!")
            return
            
        tool = self.tools[choice]
        
        print(f"\n{'='*80}")
        print(f" 🎯 Selected: {tool['name']}")
        print(f" 📋 {tool['description']}")
        print(f"{'='*80}")
        
        # Collect inputs
        inputs = self.collect_inputs(tool)
        
        # Confirm execution
        print(f"\n📊 Configuration Summary:")
        print("-" * 40)
        for key, value in inputs.items():
            print(f"   {key}: {value}")
        print("-" * 40)
        
        confirm = input("\n🤔 Execute with these settings? (y/n): ")
        if confirm.lower() not in ['y', 'yes']:
            print("❌ Execution cancelled.")
            return
            
        # Execute the tool
        self.run_tool(tool, inputs)
        
    def main_loop(self):
        """Main application loop"""
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_menu()
            
            try:
                choice = input("\n🎯 Select a tool (0-5): ")
                choice = int(choice)
                
                if choice == 0:
                    print("\n👋 Thanks for using the Automation Toolkit!")
                    print("🚀 Keep automating and stay productive!")
                    break
                elif 1 <= choice <= len(self.tools):
                    self.run_selected_tool(choice)
                    input("\n⏎ Press Enter to continue...")
                else:
                    print("\n❌ Invalid selection! Please choose 0-5.")
                    time.sleep(2)
                    
            except ValueError:
                print("\n❌ Please enter a valid number!")
                time.sleep(2)
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break

def main():
    toolkit = AutomationToolkit()
    toolkit.main_loop()

if __name__ == "__main__":
    main()
