// Chat-related utility helpers
// Centralizes ID generation and SSE parsing/unescaping so logic is not duplicated.

export function generateMessageId(): string {
  // Prefer crypto.randomUUID for better uniqueness; fallback to timestamp/random.
  if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) {
    try {
      return `msg-${crypto.randomUUID()}`;
    } catch {
      // fall through to timestamp implementation
    }
  }
  return `msg-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
}

// Unescape newline sequences that were escaped for SSE transport.
export function unescapeSseData(data: string): string {
  return data.replace(/\\n/g, '\n');
}

// Given a buffer of SSE text, extract completed data chunks (excluding [DONE]) and return remaining buffer.
export function extractSseChunks(buffer: string): { chunks: string[]; remaining: string } {
  const lines = buffer.split('\n');
  const remaining = lines.pop() || '';
  const chunks: string[] = [];
  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const payload = line.slice(6);
      if (payload && payload !== '[DONE]') {
        chunks.push(unescapeSseData(payload));
      }
    }
  }
  return { chunks, remaining };
}
