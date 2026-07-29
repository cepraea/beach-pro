import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { deflateSync } from 'node:zlib';

const outputDirectory = resolve(process.cwd(), 'public/icons');

function crc32(buffer) {
  let crc = 0xffffffff;
  for (const byte of buffer) {
    crc ^= byte;
    for (let bit = 0; bit < 8; bit += 1) {
      crc = (crc >>> 1) ^ (crc & 1 ? 0xedb88320 : 0);
    }
  }
  return (crc ^ 0xffffffff) >>> 0;
}

function chunk(type, data) {
  const typeBuffer = Buffer.from(type, 'ascii');
  const length = Buffer.alloc(4);
  length.writeUInt32BE(data.length);
  const checksum = Buffer.alloc(4);
  checksum.writeUInt32BE(crc32(Buffer.concat([typeBuffer, data])));
  return Buffer.concat([length, typeBuffer, data, checksum]);
}

function setPixel(pixels, size, x, y, red, green, blue, alpha = 255) {
  const index = (y * size + x) * 4;
  pixels[index] = red;
  pixels[index + 1] = green;
  pixels[index + 2] = blue;
  pixels[index + 3] = alpha;
}

function insideCircle(x, y, centerX, centerY, radius) {
  return (x - centerX) ** 2 + (y - centerY) ** 2 <= radius ** 2;
}

function createIcon(size) {
  const pixels = Buffer.alloc(size * size * 4);
  const center = size / 2;

  for (let y = 0; y < size; y += 1) {
    for (let x = 0; x < size; x += 1) {
      const rounded =
        insideCircle(x, y, size * 0.18, size * 0.18, size * 0.18) ||
        insideCircle(x, y, size * 0.82, size * 0.18, size * 0.18) ||
        insideCircle(x, y, size * 0.18, size * 0.82, size * 0.18) ||
        insideCircle(x, y, size * 0.82, size * 0.82, size * 0.18) ||
        (x >= size * 0.18 && x <= size * 0.82) ||
        (y >= size * 0.18 && y <= size * 0.82);

      if (!rounded) {
        setPixel(pixels, size, x, y, 0, 0, 0, 0);
        continue;
      }

      setPixel(pixels, size, x, y, 8, 67, 99);

      const waveOne = size * 0.63 + Math.sin((x / size) * Math.PI * 2) * size * 0.035;
      const waveTwo = size * 0.72 + Math.sin((x / size) * Math.PI * 2 + 1.2) * size * 0.03;
      if (Math.abs(y - waveOne) < size * 0.025 || Math.abs(y - waveTwo) < size * 0.02) {
        setPixel(pixels, size, x, y, 231, 246, 250);
      }

      if (insideCircle(x, y, center, size * 0.38, size * 0.18)) {
        setPixel(pixels, size, x, y, 244, 162, 97);
      }

      const seam = Math.abs(x - center) < size * 0.018 || Math.abs(y - size * 0.38) < size * 0.018;
      if (insideCircle(x, y, center, size * 0.38, size * 0.18) && seam) {
        setPixel(pixels, size, x, y, 8, 67, 99);
      }
    }
  }

  const rows = [];
  for (let y = 0; y < size; y += 1) {
    rows.push(Buffer.from([0]), pixels.subarray(y * size * 4, (y + 1) * size * 4));
  }

  const signature = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
  const header = Buffer.alloc(13);
  header.writeUInt32BE(size, 0);
  header.writeUInt32BE(size, 4);
  header[8] = 8;
  header[9] = 6;

  return Buffer.concat([
    signature,
    chunk('IHDR', header),
    chunk('IDAT', deflateSync(Buffer.concat(rows), { level: 9 })),
    chunk('IEND', Buffer.alloc(0)),
  ]);
}

mkdirSync(outputDirectory, { recursive: true });
for (const size of [192, 512]) {
  const output = resolve(outputDirectory, `icon-${size}x${size}.png`);
  writeFileSync(output, createIcon(size));
  console.log(`Ícone PWA gerado: ${output}`);
}
