import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const products = defineCollection({
  loader: glob({ pattern: '*.json', base: './src/data/products' }),
  schema: z.object({
    name: z.string(),
    subtitle: z.string(),
    description: z.string(),
    category: z.enum(['Electric', 'Adaptive', 'Compact', 'Sculpted']),
    subCategory: z.string().optional(),
    vendor: z.string().optional(),
    price: z.string().optional(),
    comparePrice: z.string().optional(),
    label: z.string(),
    order: z.number(),
    featured: z.boolean().default(true),
    image: z.string(),
    gallery: z.array(z.string()).min(1),
    detailImages: z.array(z.string()).optional(),
    highlights: z.array(z.object({ title: z.string(), body: z.string() })).optional(),
    features: z.array(z.string()),
    specs: z.array(z.object({ label: z.string(), value: z.string() })),
    seoTitle: z.string(),
    seoDescription: z.string(),
    note: z.string(),
  }),
});

const journal = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/data/journal' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    category: z.string(),
    image: z.string(),
    order: z.number(),
    readTime: z.string(),
    pubDate: z.string().optional().default('2026-10-14'),
    author: z.string().optional().default('BOHOL Industry Intelligence'),
    tags: z.array(z.string()).optional().default(['Manufacturing', 'Technology']),
    featured: z.boolean().optional().default(false),
    seoKeywords: z.string().optional()
  }),
});

export const collections = { products, journal };
