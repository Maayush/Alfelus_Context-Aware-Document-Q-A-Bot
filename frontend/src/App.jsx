import { useState, useRef, useEffect } from "react";
import axios from "axios";

import {
  FaRobot,
  FaUser,
  FaFilePdf,
  FaUpload,
} from "react-icons/fa";

import "./App.css";

function App() {

  const [files, setFiles] = useState([]);

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);

  const [uploading, setUploading] = useState(false);

  const chatEndRef = useRef(null);



  // =========================
  // AUTO SCROLL
  // =========================

  useEffect(() => {

    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages]);



  // =========================
  // UPLOAD FILES
  // =========================

  const uploadFiles = async (e) => {

    const uploadedFiles = Array.from(
      e.target.files
    );

    if (uploadedFiles.length === 0)
      return;

    setUploading(true);

    try {

      for (const file of uploadedFiles) {

        const formData = new FormData();

        formData.append("file", file);

        await axios.post(
          "http://127.0.0.1:8000/upload",
          formData,
          {
            headers: {
              "Content-Type":
                "multipart/form-data",
            },
          }
        );
      }

      setFiles((prev) => [

        ...prev,

        ...uploadedFiles.map(
          (file) => file.name
        ),

      ]);

      setMessages([]);

      alert(
        "Documents uploaded successfully"
      );

    } catch (error) {

      console.log(
        "UPLOAD ERROR:",
        error
      );

      alert("Upload failed");

    }

    setUploading(false);
  };



  // =========================
  // ASK QUESTION
  // =========================

  const askQuestion = async () => {

    if (!question.trim()) return;

    if (files.length === 0) {

      alert(
        "Please upload documents first"
      );

      return;
    }

    const currentQuestion = question;

    const userMessage = {

      type: "user",

      text: currentQuestion,

      time: new Date().toLocaleTimeString(),

    };

    setMessages((prev) => [

      ...prev,

      userMessage,

    ]);

    setQuestion("");

    setLoading(true);

    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/chat",
        {
          question: currentQuestion,
        }
      );

      console.log(
        "CHAT RESPONSE:",
        response.data
      );

      let finalAnswer = response.data.answer;

const hasSources =
  response.data.sources &&
  response.data.sources.length > 0;

const hasRealAnswer =
  response.data.answer &&
  response.data.answer.length > 10;

if (!hasSources && !hasRealAnswer) {

  finalAnswer =
    "This question is outside the scope of the uploaded documents.";
}

      const botMessage = {

        type: "bot",

        answer: finalAnswer,

        confidence:
          response.data.confidence || 0,

        sources:
          response.data.sources || [],

        time: new Date().toLocaleTimeString(),

      };

      setMessages((prev) => [

        ...prev,

        botMessage,

      ]);

    } catch (error) {

      console.log(
        "CHAT ERROR:",
        error
      );

      const errorMessage = {

        type: "bot",

        answer:
          "Error getting response from server.",

        confidence: 0,

        sources: [],

        time: new Date().toLocaleTimeString(),

      };

      setMessages((prev) => [

        ...prev,

        errorMessage,

      ]);
    }

    setLoading(false);
  };



  return (

    <div className="app">

      {/* SIDEBAR */}

      <div className="sidebar">

        <h2>RAG Assistant</h2>

        <label className="upload-box">

          <FaUpload />

          {
            uploading
              ? "Uploading..."
              : "Upload PDFs"
          }

          <input
            type="file"
            multiple
            hidden
            onChange={uploadFiles}
          />

        </label>



        <div className="file-list">

          {
            files.map(
              (file, index) => (

                <div
                  key={index}
                  className="file-item"
                >

                  <FaFilePdf />

                  <span>{file}</span>

                </div>
              )
            )
          }

        </div>

      </div>



      {/* CHAT AREA */}

      <div className="chat-container">

        <div className="messages">

          {
            messages.map(
              (msg, index) => (

                <div
                  key={index}
                  className={`message ${msg.type}`}
                >

                  <div className="icon">

                    {
                      msg.type === "user"
                        ? <FaUser />
                        : <FaRobot />
                    }

                  </div>



                  <div className="content">

                    {
                      msg.type === "user"
                        ? (

                          <>

                            <p>
                              {msg.text}
                            </p>

                            <div className="time">

                              {msg.time}

                            </div>

                          </>

                        ) : (

                          <>

                            <p>
                              {msg.answer}
                            </p>

                            <div className="confidence">

                              Confidence:
                              {" "}
                              {
                                Number(
                                  msg.confidence
                                ).toFixed(2)
                              }%

                            </div>

                            <div className="time">

                              {msg.time}

                            </div>



                            {
                              msg.sources &&
                              msg.sources.length > 0 && (

                                <div className="sources">

                                  <h4>
                                    Sources
                                  </h4>

                                  {
                                    msg.sources.map(
                                      (
                                        source,
                                        idx
                                      ) => (

                                        <div
                                          key={idx}
                                          className="source-card"
                                        >

                                          <div className="source-file">

                                            📄
                                            {" "}
                                            {
                                              source.file
                                            }

                                          </div>

                                          <div className="source-score">

                                            Match:
                                            {" "}
                                            {
                                              source.score
                                            }%

                                          </div>

                                          <p>

                                            {
                                              source.text
                                            }

                                          </p>

                                        </div>
                                      )
                                    )
                                  }

                                </div>
                              )
                            }

                          </>
                        )
                    }

                  </div>

                </div>
              )
            )
          }



          {
            loading && (

              <div className="loading">

                AI is thinking...

              </div>
            )
          }

          <div ref={chatEndRef}></div>

        </div>



        {/* INPUT */}

        <div className="input-area">

          <input
            type="text"
            placeholder="Ask something about documents..."
            value={question}
            onChange={(e) =>
              setQuestion(
                e.target.value
              )
            }
            onKeyDown={(e) => {

              if (
                e.key === "Enter" &&
                !loading
              ) {

                askQuestion();
              }

            }}
          />

          <button
            onClick={askQuestion}
            disabled={loading}
          >

            {
              loading
                ? "..."
                : "Send"
            }

          </button>

        </div>

      </div>

    </div>
  );
}

export default App;