import React from 'react';
import { Task } from '../types';
import { 
  CheckCircleIcon, 
  ClockIcon, 
  PencilIcon, 
  TrashIcon,
  ExclamationTriangleIcon,
  MinusCircleIcon
} from '@heroicons/react/24/outline';

interface TaskCardProps {
  task: Task;
  onToggleComplete: (taskId: string, completed: boolean) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
}

export const TaskCard: React.FC<TaskCardProps> = ({ 
  task, 
  onToggleComplete, 
  onEdit, 
  onDelete 
}) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case 'high':
        return <ExclamationTriangleIcon className="h-4 w-4 text-red-500" />;
      case 'medium':
        return <MinusCircleIcon className="h-4 w-4 text-yellow-500" />;
      case 'low':
        return <MinusCircleIcon className="h-4 w-4 text-green-500" />;
      default:
        return null;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const isOverdue = task.dueDate && new Date(task.dueDate) < new Date() && !task.completed;

  return (
    <div className={`card p-4 ${task.completed ? 'opacity-75' : ''}`}>
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3 flex-1">
          <button
            onClick={() => onToggleComplete(task.id, !task.completed)}
            className={`mt-0.5 ${
              task.completed 
                ? 'text-green-600 hover:text-green-700' 
                : 'text-gray-400 hover:text-gray-600'
            } transition-colors`}
          >
            <CheckCircleIcon className="h-5 w-5" />
          </button>
          
          <div className="flex-1 min-w-0">
            <h3 className={`text-sm font-medium ${
              task.completed ? 'line-through text-gray-500' : 'text-gray-900'
            }`}>
              {task.title}
            </h3>
            
            {task.description && (
              <p className={`mt-1 text-sm ${
                task.completed ? 'text-gray-400' : 'text-gray-600'
              }`}>
                {task.description}
              </p>
            )}
            
            <div className="mt-2 flex items-center space-x-4">
              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(task.priority)}`}>
                {getPriorityIcon(task.priority)}
                <span className="ml-1 capitalize">{task.priority}</span>
              </span>
              
              {task.dueDate && (
                <div className={`flex items-center text-xs ${
                  isOverdue ? 'text-red-600' : 'text-gray-500'
                }`}>
                  <ClockIcon className="h-3 w-3 mr-1" />
                  <span>Due {formatDate(task.dueDate)}</span>
                  {isOverdue && <span className="ml-1 font-medium">(Overdue)</span>}
                </div>
              )}
            </div>
          </div>
        </div>
        
        <div className="flex items-center space-x-2 ml-4">
          <button
            onClick={() => onEdit(task)}
            className="text-gray-400 hover:text-primary-600 transition-colors"
          >
            <PencilIcon className="h-4 w-4" />
          </button>
          <button
            onClick={() => onDelete(task.id)}
            className="text-gray-400 hover:text-red-600 transition-colors"
          >
            <TrashIcon className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
};