import os
import subprocess

def run_project():
    print("Executing End-to-End Pipeline...")
    scripts = [
        "data_pipeline.py",
        "preprocessing.py",
        "spatial_analysis.py",
        "flood_risk_model.py"
    ]
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for script in scripts:
        script_path = os.path.join(base_dir, script)
        print(f"\n--- Running {script} ---")
        subprocess.run(["python", script_path])
        
    print("\n--- Pipeline Complete! Run dashboard using: streamlit run dashboard/app.py ---")

if __name__ == "__main__":
    run_project()
