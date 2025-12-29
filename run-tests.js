const { spawn } = require('child_process');
const http = require('http');

let serverProcess = null;

// Function to check if server is ready
function checkServer(retries = 30) {
  return new Promise((resolve, reject) => {
    const attempt = () => {
      const req = http.get('http://localhost:7600', (res) => {
        console.log('Server is ready!');
        resolve();
      });

      req.on('error', () => {
        if (retries > 0) {
          console.log(`Waiting for server... (${31 - retries}/30)`);
          setTimeout(() => {
            retries--;
            attempt();
          }, 1000);
        } else {
          reject(new Error('Server failed to start'));
        }
      });
    };

    attempt();
  });
}

// Start Django server
console.log('Starting Django dev server on port 7600...');
serverProcess = spawn('pipenv', ['run', 'python', 'manage.py', 'runserver', '7600'], {
  stdio: 'pipe',
  shell: true
});

serverProcess.stdout.on('data', (data) => {
  console.log(`[SERVER] ${data}`);
});

serverProcess.stderr.on('data', (data) => {
  console.log(`[SERVER] ${data}`);
});

// Wait for server to be ready, then run tests
checkServer()
  .then(() => {
    console.log('\nRunning Playwright tests...\n');

    const testProcess = spawn('pnpm', ['exec', 'playwright', 'test', '--reporter=list'], {
      stdio: 'inherit',
      shell: true
    });

    testProcess.on('exit', (code) => {
      console.log(`\nTests completed with exit code ${code}`);

      // Kill server
      console.log('Stopping Django server...');
      if (process.platform === 'win32') {
        spawn('taskkill', ['/pid', serverProcess.pid, '/f', '/t']);
      } else {
        serverProcess.kill();
      }

      process.exit(code);
    });
  })
  .catch((err) => {
    console.error('Error:', err.message);
    if (serverProcess) {
      if (process.platform === 'win32') {
        spawn('taskkill', ['/pid', serverProcess.pid, '/f', '/t']);
      } else {
        serverProcess.kill();
      }
    }
    process.exit(1);
  });

// Handle Ctrl+C
process.on('SIGINT', () => {
  console.log('\nShutting down...');
  if (serverProcess) {
    if (process.platform === 'win32') {
      spawn('taskkill', ['/pid', serverProcess.pid, '/f', '/t']);
    } else {
      serverProcess.kill();
    }
  }
  process.exit(0);
});
