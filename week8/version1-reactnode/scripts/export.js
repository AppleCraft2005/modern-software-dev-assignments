import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { createWriteStream } from 'fs';
import { Transform } from 'stream';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.join(__dirname, '..');
const outputDir = path.join(projectRoot, 'dist');
const zipPath = path.join(outputDir, 'task-manager-project.zip');

const ignore = [
  'node_modules',
  '.git',
  'dist',
  '.env',
  '.DS_Store',
  '.bolt',
  'dist/task-manager-project.zip',
];

function createMinimalZip(sourceDir, outputPath) {
  const files = [];

  function walk(dir, prefix = '') {
    const items = fs.readdirSync(dir);

    for (const item of items) {
      if (ignore.includes(item)) continue;

      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      const relativePath = prefix ? `${prefix}/${item}` : item;

      if (stat.isDirectory()) {
        walk(fullPath, relativePath);
      } else {
        files.push({
          path: fullPath,
          name: relativePath,
        });
      }
    }
  }

  walk(sourceDir);

  const output = createWriteStream(outputPath);

  return new Promise((resolve, reject) => {
    try {
      output.write('PK\x03\x04');
      let offset = 4;
      const fileHeaders = [];

      let fileIndex = 0;
      let dataStart = 0;

      for (const file of files) {
        const content = fs.readFileSync(file.path);
        const fileName = file.name.replace(/\\/g, '/');
        const fileSize = content.length;

        const crc32 = calculateCrc32(content);
        const now = new Date();
        const dosTime = ((now.getHours() << 11) | (now.getMinutes() << 5) | (now.getSeconds() >> 1)) & 0xffff;
        const dosDate = (((now.getFullYear() - 1980) << 9) | ((now.getMonth() + 1) << 5) | now.getDate()) & 0xffff;

        const localHeader = Buffer.alloc(30 + fileName.length);
        let pos = 0;

        localHeader.writeUInt32LE(0x04034b50, pos); pos += 4;
        localHeader.writeUInt16LE(20, pos); pos += 2;
        localHeader.writeUInt16LE(0, pos); pos += 2;
        localHeader.writeUInt16LE(0, pos); pos += 2;
        localHeader.writeUInt16LE(dosTime, pos); pos += 2;
        localHeader.writeUInt16LE(dosDate, pos); pos += 2;
        localHeader.writeUInt32LE(crc32, pos); pos += 4;
        localHeader.writeUInt32LE(fileSize, pos); pos += 4;
        localHeader.writeUInt32LE(fileSize, pos); pos += 4;
        localHeader.writeUInt16LE(fileName.length, pos); pos += 2;
        localHeader.writeUInt16LE(0, pos); pos += 2;

        Buffer.from(fileName).copy(localHeader, pos);

        output.write(localHeader);
        output.write(content);

        fileHeaders.push({
          fileName,
          crc32,
          fileSize,
          offset: dataStart,
          headerSize: 30 + fileName.length,
        });

        dataStart += localHeader.length + content.length;
      }

      const cdStart = dataStart;

      for (const file of fileHeaders) {
        const cdHeader = Buffer.alloc(46 + file.fileName.length);
        let pos = 0;

        cdHeader.writeUInt32LE(0x02014b50, pos); pos += 4;
        cdHeader.writeUInt16LE(20, pos); pos += 2;
        cdHeader.writeUInt16LE(20, pos); pos += 2;
        cdHeader.writeUInt16LE(0, pos); pos += 2;
        cdHeader.writeUInt16LE(0, pos); pos += 2;

        const now = new Date();
        const dosTime = ((now.getHours() << 11) | (now.getMinutes() << 5) | (now.getSeconds() >> 1)) & 0xffff;
        const dosDate = (((now.getFullYear() - 1980) << 9) | ((now.getMonth() + 1) << 5) | now.getDate()) & 0xffff;

        cdHeader.writeUInt16LE(dosTime, pos); pos += 2;
        cdHeader.writeUInt16LE(dosDate, pos); pos += 2;
        cdHeader.writeUInt32LE(file.crc32, pos); pos += 4;
        cdHeader.writeUInt32LE(file.fileSize, pos); pos += 4;
        cdHeader.writeUInt32LE(file.fileSize, pos); pos += 4;
        cdHeader.writeUInt16LE(file.fileName.length, pos); pos += 2;
        cdHeader.writeUInt16LE(0, pos); pos += 2;
        cdHeader.writeUInt16LE(0, pos); pos += 2;
        cdHeader.writeUInt16LE(0, pos); pos += 2;
        cdHeader.writeUInt16LE(0, pos); pos += 2;
        cdHeader.writeUInt32LE(0, pos); pos += 4;
        cdHeader.writeUInt32LE(file.offset, pos); pos += 4;

        Buffer.from(file.fileName).copy(cdHeader, pos);
        output.write(cdHeader);
      }

      const cdSize = dataStart - cdStart;
      const eocd = Buffer.alloc(22);
      let pos = 0;

      eocd.writeUInt32LE(0x06054b50, pos); pos += 4;
      eocd.writeUInt16LE(0, pos); pos += 2;
      eocd.writeUInt16LE(0, pos); pos += 2;
      eocd.writeUInt16LE(fileHeaders.length, pos); pos += 2;
      eocd.writeUInt16LE(fileHeaders.length, pos); pos += 2;
      eocd.writeUInt32LE(cdSize, pos); pos += 4;
      eocd.writeUInt32LE(cdStart, pos); pos += 4;
      eocd.writeUInt16LE(0, pos);

      output.write(eocd);
      output.end();

      output.on('finish', () => {
        console.log(`Project exported to: ${outputPath}`);
        resolve();
      });
    } catch (err) {
      reject(err);
    }
  });
}

function calculateCrc32(buf) {
  let crc = 0 ^ (-1);

  for (let i = 0; i < buf.length; i++) {
    const byte = buf[i];
    crc = (crc >>> 8) ^ ((crc ^ byte) & 0xFF);
    for (let j = 0; j < 8; j++) {
      crc = (crc >>> 1) ^ (((crc & 1) === 1) ? 0xedb88320 : 0);
    }
  }

  return (crc ^ (-1)) >>> 0;
}

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

createMinimalZip(projectRoot, zipPath)
  .then(() => {
    const stats = fs.statSync(zipPath);
    console.log(`File size: ${(stats.size / 1024).toFixed(2)} KB`);
    console.log('\nYour project is ready to download!');
  })
  .catch(err => {
    console.error('Error creating ZIP:', err);
    process.exit(1);
  });
