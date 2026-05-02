import {z} from 'zod';

export const MappingSchema = z.object({
  question: z.string().nullable(),
  index: z.int32().nullable(),
  type:z.enum(["ordinal", "nominal", "continuous", "text"]).nullable(), 
  unique_count: z.int32().nullable(),
  missing_count: z.int32().nullable(),
  total_count: z.int32().nullable(),
  ignored: z.boolean(),
  cafeteria: z.array(z.record(z.string(), z.any())).nullable(),
  cafeteria_dump: z.array(z.record(z.string(), z.any())).nullable(),
  subquestions: z.array(z.record(z.string(), z.any())).nullable(),
  is_maq: z.boolean(),
})

export const CafeteriaSchema = z.object({
  vaule: z.string().nullable(),
  index: z.int32().nullable(),
  n: z.int32().nullable(),
  pct: z.float32().nullable(),
  is_missing: z.boolean().nullable(),
  missing_code: z.string().nullable() ?? z.int32().nullable(),
})

export const SurveyQuestion = z.object({
  text: z.string(),
  index: z.int32(),
  question_type: z.enum(["single", "maq", "text", "table", "numerical"]),
  cafeteria: z.array(z.record(z.string(), z.any())).nullable(),
  columns:  z.array(z.record(z.string(), z.any())).nullable(),
  is_showable: z.boolean()
})