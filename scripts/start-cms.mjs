import {spawn} from 'node:child_process';
// Allow both localhost and 127.0.0.1 on any port by omitting restricted ORIGIN
const child=spawn(process.execPath,['node_modules/decap-server/dist/index.js'],{
  stdio:'inherit',
  env:{...process.env,BIND_HOST:'127.0.0.1',PORT:'8081'}
});
child.on('exit',code=>process.exit(code??0));
