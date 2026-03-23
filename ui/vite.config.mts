import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/suppliers': 'http://127.0.0.1:8000',
      '/products': 'http://127.0.0.1:8000',
      '/warehouses': 'http://127.0.0.1:8000',
      '/employees': 'http://127.0.0.1:8000',
      '/inventory': 'http://127.0.0.1:8000',
      '/transactions': 'http://127.0.0.1:8000',
      '/categories': 'http://127.0.0.1:8000',
      '/roles': 'http://127.0.0.1:8000',
      '/stock-movements': 'http://127.0.0.1:8000',
      '/products-detailed': 'http://127.0.0.1:8000',
      '/employees-detailed': 'http://127.0.0.1:8000',
      '/health': 'http://127.0.0.1:8000',
    }
  },
});