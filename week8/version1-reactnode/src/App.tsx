import { useEffect, useState } from 'react';
import { CheckSquare } from 'lucide-react';
import { supabase, Task } from './lib/supabase';
import { TaskForm } from './components/TaskForm';
import { TaskItem } from './components/TaskItem';

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const { data, error: fetchError } = await supabase
        .from('tasks')
        .select('*')
        .order('created_at', { ascending: false });

      if (fetchError) throw fetchError;
      setTasks(data || []);
    } catch (err) {
      setError('Failed to load tasks. Please refresh the page.');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const createTask = async (title: string, description: string) => {
    try {
      const { data, error: insertError } = await supabase
        .from('tasks')
        .insert([{ title, description }])
        .select()
        .single();

      if (insertError) throw insertError;
      if (data) {
        setTasks([data, ...tasks]);
      }
    } catch (err) {
      console.error('Error creating task:', err);
      throw err;
    }
  };

  const toggleTaskComplete = async (id: string, completed: boolean) => {
    try {
      const { error: updateError } = await supabase
        .from('tasks')
        .update({ completed, updated_at: new Date().toISOString() })
        .eq('id', id);

      if (updateError) throw updateError;

      setTasks(tasks.map((task) =>
        task.id === id ? { ...task, completed, updated_at: new Date().toISOString() } : task
      ));
    } catch (err) {
      setError('Failed to update task. Please try again.');
      console.error('Error updating task:', err);
    }
  };

  const deleteTask = async (id: string) => {
    try {
      const { error: deleteError } = await supabase
        .from('tasks')
        .delete()
        .eq('id', id);

      if (deleteError) throw deleteError;
      setTasks(tasks.filter((task) => task.id !== id));
    } catch (err) {
      setError('Failed to delete task. Please try again.');
      console.error('Error deleting task:', err);
    }
  };

  const completedTasks = tasks.filter((task) => task.completed).length;
  const totalTasks = tasks.length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-8 px-4">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-2">
            <CheckSquare size={40} className="text-blue-600" />
            <h1 className="text-4xl font-bold text-gray-800">Task Manager</h1>
          </div>
          <p className="text-gray-600">Stay organized and productive</p>
          {totalTasks > 0 && (
            <div className="mt-3 text-sm text-gray-500">
              {completedTasks} of {totalTasks} tasks completed
            </div>
          )}
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        <TaskForm onSubmit={createTask} />

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Loading tasks...</p>
          </div>
        ) : tasks.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow-md">
            <CheckSquare size={48} className="mx-auto text-gray-300 mb-4" />
            <h3 className="text-xl font-semibold text-gray-600 mb-2">No tasks yet</h3>
            <p className="text-gray-500">Create your first task to get started!</p>
          </div>
        ) : (
          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Your Tasks</h2>
            {tasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onToggleComplete={toggleTaskComplete}
                onDelete={deleteTask}
              />
            ))}
          </div>
        )}

      </div>
    </div>
  );
}

export default App;
