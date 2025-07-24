import React, { useState, useEffect } from 'react';
import { AxiosError } from 'axios';
import { Task, CreateTaskData, UpdateTaskData, ApiError } from '../types';
import { tasksAPI } from '../utils/api';
import { Layout } from '../components/Layout';
import { TaskCard } from '../components/TaskCard';
import { TaskForm } from '../components/TaskForm';
import { Modal } from '../components/Modal';
import { PlusIcon } from '@heroicons/react/24/outline';

export const Dashboard: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const data = await tasksAPI.getTasks();
      setTasks(data);
      setError('');
    } catch (err) {
      const error = err as AxiosError<ApiError>;
      setError(error.response?.data?.error || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (data: CreateTaskData) => {
    try {
      const newTask = await tasksAPI.createTask(data);
      setTasks([newTask, ...tasks]);
      setIsCreateModalOpen(false);
    } catch (err) {
      const error = err as AxiosError<ApiError>;
      setError(error.response?.data?.error || 'Failed to create task');
      throw err;
    }
  };

  const handleUpdateTask = async (data: UpdateTaskData) => {
    if (!editingTask) return;

    try {
      const updatedTask = await tasksAPI.updateTask(editingTask.id, data);
      setTasks(tasks.map(task => task.id === editingTask.id ? updatedTask : task));
      setIsEditModalOpen(false);
      setEditingTask(null);
    } catch (err) {
      const error = err as AxiosError<ApiError>;
      setError(error.response?.data?.error || 'Failed to update task');
      throw err;
    }
  };

  const handleToggleComplete = async (taskId: string, completed: boolean) => {
    try {
      const updatedTask = await tasksAPI.updateTask(taskId, { completed });
      setTasks(tasks.map(task => task.id === taskId ? updatedTask : task));
    } catch (err) {
      const error = err as AxiosError<ApiError>;
      setError(error.response?.data?.error || 'Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      await tasksAPI.deleteTask(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      const error = err as AxiosError<ApiError>;
      setError(error.response?.data?.error || 'Failed to delete task');
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setIsEditModalOpen(true);
  };

  const filteredTasks = tasks.filter(task => {
    switch (filter) {
      case 'pending':
        return !task.completed;
      case 'completed':
        return task.completed;
      default:
        return true;
    }
  });

  const taskStats = {
    total: tasks.length,
    completed: tasks.filter(task => task.completed).length,
    pending: tasks.filter(task => !task.completed).length,
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">My Tasks</h2>
            <p className="text-gray-600">
              {taskStats.total} total, {taskStats.pending} pending, {taskStats.completed} completed
            </p>
          </div>
          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="btn-primary flex items-center space-x-2"
          >
            <PlusIcon className="h-5 w-5" />
            <span>New Task</span>
          </button>
        </div>

        {/* Error display */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {/* Filter tabs */}
        <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg w-fit">
          {(['all', 'pending', 'completed'] as const).map((filterOption) => (
            <button
              key={filterOption}
              onClick={() => setFilter(filterOption)}
              className={`px-3 py-1 text-sm font-medium rounded-md transition-colors ${
                filter === filterOption
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              {filterOption.charAt(0).toUpperCase() + filterOption.slice(1)}
            </button>
          ))}
        </div>

        {/* Tasks list */}
        <div className="space-y-3">
          {filteredTasks.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500">
                {filter === 'all' 
                  ? 'No tasks yet. Create your first task!' 
                  : `No ${filter} tasks.`}
              </p>
            </div>
          ) : (
            filteredTasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onToggleComplete={handleToggleComplete}
                onEdit={handleEditTask}
                onDelete={handleDeleteTask}
              />
            ))
          )}
        </div>

        {/* Create Task Modal */}
        <Modal
          isOpen={isCreateModalOpen}
          onClose={() => setIsCreateModalOpen(false)}
          title="Create New Task"
        >
          <TaskForm
            onSubmit={handleCreateTask}
            onCancel={() => setIsCreateModalOpen(false)}
          />
        </Modal>

        {/* Edit Task Modal */}
        <Modal
          isOpen={isEditModalOpen}
          onClose={() => {
            setIsEditModalOpen(false);
            setEditingTask(null);
          }}
          title="Edit Task"
        >
          {editingTask && (
            <TaskForm
              onSubmit={handleUpdateTask}
              onCancel={() => {
                setIsEditModalOpen(false);
                setEditingTask(null);
              }}
              initialData={editingTask}
              isEditing
            />
          )}
        </Modal>
      </div>
    </Layout>
  );
};