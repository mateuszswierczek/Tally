import {z} from 'zod';

export const MappingSchema = z.object({
  question: z.string().nullable(),
  index: z.int32().nullable(),
  type: z.string().nullable(),
  unique_count: z.int32().nullable(),
  missing_count: z.int32().nullable(),
  total_count: z.int32().nullable(),
  ignored: z.boolean(),
  cafeteria: z.array(z.record(z.string(), z.any())).nullable(),
  cafeteria_dump: z.array(z.record(z.string(), z.any())).nullable(),
  subquestions: z.array(z.record(z.string(), z.any())).nullable()
})

