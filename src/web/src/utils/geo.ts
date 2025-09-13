import slugify from "slugify";

export function isPostcode(input: string) {
  const v = input.trim();
  // Postcodes are 4 digits in Australia
  return /^\d{4}$/.test(v);
}

export function toSlug(name: string) {
  return slugify(name, {
    lower: true,
    strict: true,
    trim: true,
  });
}
