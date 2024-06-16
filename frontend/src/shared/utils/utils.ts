export function uuidv4(): string {
  const hex = Array.from({ length: 256 }, (_, index) =>
    index.toString(16).padStart(2, "0")
  );

  const r = crypto.getRandomValues(new Uint8Array(16));

  r[6] = (r[6] & 0x0f) | 0x40;
  r[8] = (r[8] & 0x3f) | 0x80;

  const segments = Array.from(r, (value, index) => {
    const hexValue = hex[value];
    return [4, 6, 8, 10].includes(index) ? `-${hexValue}` : hexValue;
  });

  return segments.join("");
}
