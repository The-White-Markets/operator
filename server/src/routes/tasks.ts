import { Router, Response } from 'express';
import { PrismaClient } from '@prisma/client';
import { z } from 'zod';
import { AuthRequest, CreateTaskData, UpdateTaskData } from '../types';
import { authenticateToken } from '../middleware/auth';

const router = Router();
const prisma = new PrismaClient();

// Validation schemas
const createTaskSchema = z.object({
  title: z.string().min(1).max(200),
  description: z.string().optional(),
  priority: z.enum(['low', 'medium', 'high']).optional(),
  dueDate: z.string().datetime().optional()
});

const updateTaskSchema = z.object({
  title: z.string().min(1).max(200).optional(),
  description: z.string().optional(),
  completed: z.boolean().optional(),
  priority: z.enum(['low', 'medium', 'high']).optional(),
  dueDate: z.string().datetime().optional()
});

// Apply authentication middleware to all routes
router.use(authenticateToken);

// Get all tasks for authenticated user
router.get('/', async (req: AuthRequest, res: Response) => {
  try {
    const tasks = await prisma.task.findMany({
      where: { userId: req.userId },
      orderBy: [
        { completed: 'asc' },
        { createdAt: 'desc' }
      ]
    });

    res.json(tasks);
  } catch (error) {
    console.error('Get tasks error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get single task
router.get('/:id', async (req: AuthRequest, res: Response) => {
  try {
    const task = await prisma.task.findFirst({
      where: {
        id: req.params.id,
        userId: req.userId
      }
    });

    if (!task) {
      return res.status(404).json({ error: 'Task not found' });
    }

    res.json(task);
  } catch (error) {
    console.error('Get task error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Create new task
router.post('/', async (req: AuthRequest, res: Response) => {
  try {
    const validatedData = createTaskSchema.parse(req.body) as CreateTaskData;

    const task = await prisma.task.create({
      data: {
        title: validatedData.title,
        description: validatedData.description,
        priority: validatedData.priority || 'medium',
        dueDate: validatedData.dueDate ? new Date(validatedData.dueDate) : null,
        userId: req.userId!
      }
    });

    res.status(201).json(task);
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ error: 'Validation failed', details: error.errors });
    }
    console.error('Create task error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Update task
router.put('/:id', async (req: AuthRequest, res: Response) => {
  try {
    const validatedData = updateTaskSchema.parse(req.body) as UpdateTaskData;

    // Check if task exists and belongs to user
    const existingTask = await prisma.task.findFirst({
      where: {
        id: req.params.id,
        userId: req.userId
      }
    });

    if (!existingTask) {
      return res.status(404).json({ error: 'Task not found' });
    }

    const updatedTask = await prisma.task.update({
      where: { id: req.params.id },
      data: {
        ...validatedData,
        dueDate: validatedData.dueDate ? new Date(validatedData.dueDate) : undefined
      }
    });

    res.json(updatedTask);
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ error: 'Validation failed', details: error.errors });
    }
    console.error('Update task error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Delete task
router.delete('/:id', async (req: AuthRequest, res: Response) => {
  try {
    // Check if task exists and belongs to user
    const existingTask = await prisma.task.findFirst({
      where: {
        id: req.params.id,
        userId: req.userId
      }
    });

    if (!existingTask) {
      return res.status(404).json({ error: 'Task not found' });
    }

    await prisma.task.delete({
      where: { id: req.params.id }
    });

    res.json({ message: 'Task deleted successfully' });
  } catch (error) {
    console.error('Delete task error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

export default router;