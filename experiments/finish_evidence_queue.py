"""Continue the fixed queue after the already-running controlled experiment."""
import argparse,ctypes,datetime,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def count(p):return len(p.read_bytes().splitlines()) if p.exists() else 0
def run(*args):
    print('RUN',*args,flush=True)
    subprocess.run([sys.executable,'-B',str(ROOT/args[0]),*args[1:]],check=True,cwd=ROOT)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--wait-pid',type=int,required=True);a=ap.parse_args()
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    kernel.OpenProcess.argtypes=[ctypes.c_ulong,ctypes.c_bool,ctypes.c_ulong];kernel.OpenProcess.restype=ctypes.c_void_p
    kernel.WaitForSingleObject.argtypes=[ctypes.c_void_p,ctypes.c_ulong];kernel.CloseHandle.argtypes=[ctypes.c_void_p]
    handle=kernel.OpenProcess(0x100000,False,a.wait_pid)
    if handle:
        start=time.monotonic()
        try:
            while kernel.WaitForSingleObject(handle,5000)==258:
                if time.monotonic()-start>10800:raise TimeoutError('Three-hour guard waiting for fixed inference queue')
        finally:kernel.CloseHandle(handle)
    for kind in ['direct','checklist']:
        assert count(ROOT/'outputs'/f'qwen14_controlled_cases_{kind}.jsonl')==108,'Incomplete controlled run; no silent resume or scoring'
    run('analyze_evidence_audit.py','--dataset',str(ROOT/'controlled_cases.jsonl'),'--pairs',str(ROOT/'constructed_pairs.jsonl'),'--output-tag','frozen_reference')
    run('analyze_evidence_audit.py','--dataset',str(ROOT/'controlled_cases.jsonl'),'--pairs',str(ROOT/'constructed_pairs.jsonl'),'--erratum',str(ROOT/'annotation_erratum.json'))
    run('analyze_evidence_audit.py','--dataset',str(ROOT/'controlled_cases.jsonl'),'--pairs',str(ROOT/'constructed_pairs.jsonl'),'--erratum',str(ROOT/'annotation_erratum.json'),'--exclude-family','frame_species','--output-tag','excluding_frame_species')
    run('run_evidence_audit.py','--model','qwen14','--dataset',str(ROOT/'source_recovery_cases.jsonl'))
    run('analyze_evidence_audit.py','--dataset',str(ROOT/'source_recovery_cases.jsonl'),'--pairs',str(ROOT/'source_recovery_pairs.jsonl'))
    run('write_experiment_report.py')
    print('FIXED QUEUE COMPLETE',datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
if __name__=='__main__':main()
