# Task Manager Application

A full-stack task management application built with React, TypeScript, Supabase, and Tailwind CSS.

## Features

- Create new tasks with title and description
- Mark tasks as complete/incomplete
- Delete tasks with confirmation
- View all tasks with completion progress
- Persistent storage with Supabase
- Clean, modern UI with Tailwind CSS
- Full CRUD operations with validation and error handling
- Responsive design for all screen sizes

## Tech Stack

- **Frontend**: React 18, TypeScript, Vite
- **Database**: Supabase (PostgreSQL)
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Backend**: Supabase (serverless)

## Project Structure

```
src/
├── components/
│   ├── TaskForm.tsx      # Form for creating new tasks
│   ├── TaskItem.tsx      # Individual task card component
│   └── DownloadButton.tsx # Download project button
├── lib/
│   └── supabase.ts       # Supabase client configuration
├── App.tsx               # Main application component
├── main.tsx              # React entry point
└── index.css             # Global styles
```

## Setup Instructions

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Verify the `.env` file contains:
   ```
   VITE_SUPABASE_URL=your_supabase_url
   VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

3. The database migration is automatically applied to Supabase. The `tasks` table includes:
   - `id`: UUID primary key
   - `title`: Task title (required)
   - `description`: Task description (optional)
   - `completed`: Completion status (boolean)
   - `created_at`: Creation timestamp
   - `updated_at`: Last update timestamp

### Running the Application

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173` (or the URL shown in terminal).

### Building for Production

```bash
npm run build
```

This creates an optimized production build in the `dist/` folder.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run typecheck` - Check TypeScript types
- `npm run export` - Export project as ZIP file

## Usage

1. **Create a Task**:
   - Enter a title (required) and optional description
   - Click "Add Task"
   - Title validation ensures tasks have meaningful names

2. **Complete a Task**:
   - Click the circle icon next to a task to mark it complete
   - Completed tasks show a green checkmark and strike-through text

3. **Delete a Task**:
   - Click the trash icon to delete a task
   - Confirm deletion in the dialog

4. **Track Progress**:
   - View the completion count at the top of the app
   - Shows "X of Y tasks completed"

## Validation & Error Handling

- **Title Validation**: Empty titles are rejected with a clear error message
- **Error Messages**: Network and database errors display helpful feedback
- **Loading States**: Visual feedback during data operations
- **Confirmation Dialogs**: Delete actions require confirmation to prevent accidents

## Database Schema

### tasks table

```sql
CREATE TABLE tasks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL,
  description text DEFAULT '',
  completed boolean DEFAULT false,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);
```

All tasks are publicly accessible. Row-level security (RLS) allows anyone to view, create, update, and delete tasks.

## Customization

### Styling

The application uses Tailwind CSS. Customize colors and styles by editing:
- `src/index.css` - Global styles
- Component files - Component-specific styles
- `tailwind.config.js` - Tailwind configuration

### Environment Variables

Required environment variables in `.env`:
- `VITE_SUPABASE_URL` - Your Supabase project URL
- `VITE_SUPABASE_ANON_KEY` - Your Supabase anonymous key

## Performance

- Optimized bundle size (~280KB gzipped)
- Efficient database queries with proper indexing
- Lazy loading and code splitting via Vite
- Real-time UI updates with React hooks

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT

## Support

For issues or questions, refer to the source code in the `src/` directory. Each component is well-documented and straightforward to modify.
