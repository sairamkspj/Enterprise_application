import { Component, ViewChild, ElementRef } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { logfile_Service } from './logfileservice';
import { HttpClient } from '@angular/common/http';
import { interval, Subscription } from 'rxjs';
import { Chart, ChartType, registerables } from 'chart.js';

Chart.register(...registerables);

interface LogEntry {
  Critical?: number;
  Error?: number;
  Warning?: number;
  Information?: number;
  Unknown?: number;
  'Audit Success'?: number;
  'Audit Failure'?: number;
}

interface LogCounts {
  [key: string]: LogEntry | undefined;
}

@Component({
  selector: 'app-log-upload',
  imports: [FormsModule, CommonModule, ReactiveFormsModule],
  templateUrl: './log-file.html',
  styleUrls: ['./log-file.css'],
})
export class LogUploadComponent {
  logSource = 'windows';
  response: any = null;
  pollingSub: Subscription | null = null;
  counts: LogCounts = {};
  chart: Chart | null = null;
  unusualLogs: any[] = [];
  selectedFile: File | null = null;

  @ViewChild('logChart', { static: false }) chartRef!: ElementRef<HTMLCanvasElement>;

  constructor(private log_service: logfile_Service, private http: HttpClient) {}

  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    if (file) this.selectedFile = file;
  }

  onUpload() {
    if (!this.selectedFile) return;

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.log_service.Send_data(formData).subscribe({
      next: (response: any[]) => {
        this.unusualLogs = response;
      },
      error: (err) => console.error('Upload failed', err),
    });
  }

  processLogs() {
    this.response = 'Processing...';
    this.counts = {};

    this.log_service.processLogs(this.logSource).subscribe(
      (res: any) => {
        this.response = res;

        if (res.task_id) {
          this.pollTask(res.task_id);
        } else if (res.result) {
          this.counts = res.result;
          setTimeout(() => this.renderChart(), 0);
        }
      },
      (err) => {
        this.response = 'Error: ' + err.message;
      }
    );
  }

  pollTask(taskId: string) {
    const source = interval(1000);
    this.pollingSub = source.subscribe(() => {
      this.log_service.getTaskStatus(taskId).subscribe((res: any) => {
        this.response = res;

        if (res.state === 'SUCCESS' && res.result) {
          this.counts = res.result;
          setTimeout(() => this.renderChart(), 0);
          if (this.pollingSub) this.pollingSub.unsubscribe();
        }
      });
    });
  }

  renderChart() {
    if (!this.counts || !this.chartRef) return;

    const logKeys = ['Application', 'System', 'Setup', 'Security'];
    const labels = logKeys.filter((log) => this.counts[log] !== undefined);

    const critical: number[] = [];
    const error: number[] = [];
    const warning: number[] = [];
    const info: number[] = [];
    const unknown: number[] = [];

    for (const log of labels) {
      const entry = this.counts[log]!;

      if (log === 'Security') {
        critical.push(entry['Audit Success'] ?? 0);
        error.push(entry['Audit Failure'] ?? 0);
        warning.push(0);
        info.push(0);
        unknown.push(entry.Unknown ?? 0);
      } else {
        critical.push(entry.Critical ?? 0);
        error.push(entry.Error ?? 0);
        warning.push(entry.Warning ?? 0);
        info.push(entry.Information ?? 0);
        unknown.push(entry.Unknown ?? 0);
      }
    }

    if (this.chart) {
      this.chart.destroy();
      this.chart = null;
    }

    const canvas = this.chartRef.nativeElement;
    this.chart = new Chart(canvas, {
      type: 'bar' as ChartType,
      data: {
        labels,
        datasets: [
          { label: 'Critical / Audit Success', data: critical, backgroundColor: 'red' },
          { label: 'Error / Audit Failure', data: error, backgroundColor: 'orange' },
          { label: 'Warning', data: warning, backgroundColor: 'yellow' },
          { label: 'Information', data: info, backgroundColor: 'blue' },
          { label: 'Unknown', data: unknown, backgroundColor: 'gray' },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { position: 'top' } },
        scales: { x: { stacked: true }, y: { stacked: true, beginAtZero: true } },
      },
    });
  }
}
