import {
  FaUserCircle,
  FaEnvelope,
  FaPhone,
  FaGraduationCap,
  FaMapMarkerAlt,
  FaBriefcase,
  FaEdit,
} from "react-icons/fa";

function Profile() {
  return (
    <div className="min-h-screen bg-slate-950 p-8">

      <div className="max-w-5xl mx-auto bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-lg">

        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">

          <div className="flex items-center gap-6">

            <FaUserCircle className="text-8xl text-cyan-400" />

            <div>

              <h1 className="text-4xl font-bold text-white">
                Abdul
              </h1>

              <p className="text-gray-400 mt-1">
                AI & Machine Learning Enthusiast
              </p>

            </div>

          </div>

          <button className="flex items-center gap-2 bg-cyan-500 hover:bg-cyan-600 px-5 py-3 rounded-lg text-white transition">
            <FaEdit />
            Edit Profile
          </button>

        </div>

        {/* Profile Details */}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-10">

          <div className="bg-slate-800 rounded-xl p-5">

            <div className="flex items-center gap-3 text-white mb-4">
              <FaEnvelope className="text-cyan-400" />
              <span>abdul@gmail.com</span>
            </div>

            <div className="flex items-center gap-3 text-white mb-4">
              <FaPhone className="text-cyan-400" />
              <span>+91 9876543210</span>
            </div>

            <div className="flex items-center gap-3 text-white">
              <FaMapMarkerAlt className="text-cyan-400" />
              <span>Coimbatore, Tamil Nadu</span>
            </div>

          </div>

          <div className="bg-slate-800 rounded-xl p-5">

            <div className="flex items-center gap-3 text-white mb-4">
              <FaGraduationCap className="text-cyan-400" />
              <span>B.E. Computer Science Engineering</span>
            </div>

            <div className="flex items-center gap-3 text-white mb-4">
              <FaBriefcase className="text-cyan-400" />
              <span>Aspiring Machine Learning Engineer</span>
            </div>

            <div className="flex items-center gap-3 text-white">
              <FaUserCircle className="text-cyan-400" />
              <span>Resume Uploaded: Yes</span>
            </div>

          </div>

        </div>

      </div>

    </div>
  );
}

export default Profile;