import React, { useState } from "react";

function FileUpload({ onUpload }) {
  const [file, setFile] = useState(null);

  const handleChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) onUpload(file);
  };

  return (
    <div className="bg-white shadow-md p-6 rounded-2xl w-full max-w-md">
      <h2 className="text-xl font-semibold mb-4 text-gray-800 text-center">
        Upload your document
      </h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          type="file"
          accept=".pdf,image/*"
          onChange={handleChange}
          className="border border-gray-300 rounded-lg p-2 cursor-pointer"
        />
        <button
          type="submit"
          className="bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition duration-200"
        >
          Generate Summary
        </button>
      </form>
    </div>
  );
}

export default FileUpload;
