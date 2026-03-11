import { Trash2, CheckCircle, Circle } from 'lucide-react';
import { Task } from '../lib/supabase';

interface TaskItemProps {
  task: Task;
  onToggleComplete: (id: string, completed: boolean) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
}

export function TaskItem({ task, onToggleComplete, onDelete }: TaskItemProps) {
  const handleToggle = async () => {
    await onToggleComplete(task.id, !task.completed);
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      await onDelete(task.id);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-5 mb-3 transition hover:shadow-lg">
      <div className="flex items-start gap-4">
        <button
          onClick={handleToggle}
          className="flex-shrink-0 mt-1 text-gray-400 hover:text-blue-600 transition"
          aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
        >
          {task.completed ? (
            <CheckCircle size={24} className="text-green-600" />
          ) : (
            <Circle size={24} />
          )}
        </button>

        <div className="flex-grow">
          <h3
            className={`text-lg font-semibold ${
              task.completed ? 'text-gray-400 line-through' : 'text-gray-800'
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p
              className={`mt-1 text-sm ${
                task.completed ? 'text-gray-400' : 'text-gray-600'
              }`}
            >
              {task.description}
            </p>
          )}
          <p className="mt-2 text-xs text-gray-400">
            Created: {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>

        <button
          onClick={handleDelete}
          className="flex-shrink-0 text-gray-400 hover:text-red-600 transition"
          aria-label="Delete task"
        >
          <Trash2 size={20} />
        </button>
      </div>
    </div>
  );
}
