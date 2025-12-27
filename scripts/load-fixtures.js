// Cross-platform script to load Django fixtures
const { execSync } = require('child_process');
const path = require('path');

const isWindows = process.platform === 'win32';
const scriptName = isWindows ? 'load_fixtures.ps1' : 'load_fixtures.sh';
const scriptPath = path.join(__dirname, '..', scriptName);

try {
  if (isWindows) {
    execSync(`powershell -ExecutionPolicy Bypass -File "${scriptPath}"`, {
      stdio: 'inherit',
      cwd: path.join(__dirname, '..')
    });
  } else {
    execSync(`bash "${scriptPath}"`, {
      stdio: 'inherit',
      cwd: path.join(__dirname, '..')
    });
  }
} catch (error) {
  console.error('Error loading fixtures:', error.message);
  process.exit(1);
}

