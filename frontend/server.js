const express = require('express');
const path = require('path');

const app = express();
app.use(express.static(path.join(__dirname, 'UI-1')));

const preferredPort = parseInt(process.env.PORT, 10) || 5600;

function start(port) {
  const server = app.listen(port, () => {
    console.log(`Frontend server is running at http://localhost:${port}/`);
  });

  server.on('error', (err) => {
    if (err && err.code === 'EADDRINUSE') {
      const next = port + 1;
      console.warn(`Port ${port} in use, trying ${next}...`);
      start(next);
    } else {
      console.error(err);
    }
  });
}

start(preferredPort);