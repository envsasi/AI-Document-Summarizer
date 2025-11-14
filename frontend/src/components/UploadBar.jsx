import React, { useRef, useState } from "react";
import { UploadCloud } from "lucide-react";

export default function UploadBar({ onUpload }) {
  const [file, setFile] = useState(null);
  const [length, setLength] = useState("medium");
  const inputRef = useRef();
  const [dragging, setDragging] = useState(false);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);

    if (e.dataTransfer.files.length === 0) return;
    setFile(e.dataTransfer.files[0]);
  };

  const send = () => {
    if (!file) return alert("Please choose a document.");
    onUpload(file, length);
    setFile(null);
    inputRef.current.value = null;
  };

  return (
    <div
      className="border-t bg-white p-4 flex flex-col gap-3"
      onDragOver={(e) => {
        e.preventDefault();
        setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
    >
      {dragging && (
        <div className="p-4 border-2 border-dashed border-blue-600 rounded-xl text-center text-blue-600 font-semibold bg-blue-50">
          Drop your PDF/Image here…
        </div>
      )}

      {!dragging && (
        <div className="flex items-center gap-4">
          <input
            ref={inputRef}
            type="file"
            accept=".pdf, image/*"
            onChange={(e) => setFile(e.target.files[0])}
            className="hidden"
          />

          <button
            onClick={() => inputRef.current.click()}
            className="p-3 bg-gray-100 rounded-xl hover:bg-gray-200"
          >
            <UploadCloud className="w-5 h-5" />
          </button>

          <div className="flex-1 text-sm text-gray-600">
            {file ? file.name : "Upload document… or drag & drop"}
          </div>

          <select
            value={length}
            onChange={(e) => setLength(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm"
          >
            <option value="short">Short</option>
            <option value="medium">Medium</option>
            <option value="long">Long</option>
          </select>

          <button
            onClick={send}
            className="px-6 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700"
          >
            Summarize
          </button>
        </div>
      )}
    </div>
  );
}
