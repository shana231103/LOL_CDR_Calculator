// File: frontend/src/utils/text.js

/**
 * Normalizes text by removing Vietnamese accents/diacritics and lowercasing.
 * e.g. "Ngộ Không" -> "ngo khong", "Lee Sin" -> "lee sin"
 */
export function normalizeText(str) {
  if (!str) return ''
  return str
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim()
}
