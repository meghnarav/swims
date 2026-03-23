import { useState } from "react";

export default function AddEmployeeForm({ roles, onSuccess }) {
  const [name, setName]           = useState("");
  const [roleId, setRoleId]       = useState("");
  const [empType, setEmpType]     = useState("permanent");

  // Permanent fields
  const [salary, setSalary]       = useState("");
  const [benefits, setBenefits]   = useState("");

  // Contract fields
  const [hourlyRate, setHourlyRate]       = useState("");
  const [contractEnd, setContractEnd]     = useState("");

  const [status, setStatus]       = useState("");
  const [loading, setLoading]     = useState(false);

  const handleSubmit = async () => {
    if (!name || !roleId) {
      setStatus("⚠️ Name and Role are required.");
      return;
    }

    setLoading(true);
    setStatus("");

    try {
      // 1. Create base employee
      const empRes = await fetch("/employees", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, role_id: parseInt(roleId) }),
      });

      if (!empRes.ok) throw new Error("Failed to create employee.");
      const emp = await empRes.json();
      const empId = emp.employee_id;

      // 2. Create subtype record
      if (empType === "permanent") {
        await fetch("/employees/permanent", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            employee_id:    empId,
            monthly_salary: parseFloat(salary) || null,
            benefits:       benefits || null,
          }),
        });
      } else {
        await fetch("/employees/contract", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            employee_id:       empId,
            hourly_rate:       parseFloat(hourlyRate) || null,
            contract_end_date: contractEnd || null,
          }),
        });
      }

      setStatus("✅ Employee added successfully!");
      setName(""); setRoleId(""); setSalary("");
      setBenefits(""); setHourlyRate(""); setContractEnd("");
      if (onSuccess) onSuccess();

    } catch (err) {
      setStatus("❌ Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>Add Employee</h2>
      <div className="form">

        {/* Name */}
        <div className="form-row">
          <label>Name *</label>
          <input
            value={name}
            onChange={e => setName(e.target.value)}
            placeholder="Full name"
          />
        </div>

        {/* Role */}
        <div className="form-row">
          <label>Role *</label>
          <select value={roleId} onChange={e => setRoleId(e.target.value)}>
            <option value="">Select role...</option>
            {roles.map(r => (
              <option key={r.role_id} value={r.role_id}>{r.role_name}</option>
            ))}
          </select>
        </div>

        {/* Employee Type Toggle */}
        <div className="form-row">
          <label>Employee Type</label>
          <div className="toggle-group">
            <button
              type="button"
              className={`toggle-btn ${empType === "permanent" ? "active" : ""}`}
              onClick={() => setEmpType("permanent")}
            >
              Permanent
            </button>
            <button
              type="button"
              className={`toggle-btn ${empType === "contract" ? "active" : ""}`}
              onClick={() => setEmpType("contract")}
            >
              Contract
            </button>
          </div>
        </div>

        {/* Permanent Fields */}
        {empType === "permanent" && (
          <>
            <div className="form-row">
              <label>Monthly Salary (₹)</label>
              <input
                type="number"
                value={salary}
                onChange={e => setSalary(e.target.value)}
                placeholder="e.g. 60000"
                min="0"
              />
            </div>
            <div className="form-row">
              <label>Benefits</label>
              <input
                value={benefits}
                onChange={e => setBenefits(e.target.value)}
                placeholder="e.g. Health Insurance"
              />
            </div>
          </>
        )}

        {/* Contract Fields */}
        {empType === "contract" && (
          <>
            <div className="form-row">
              <label>Hourly Rate (₹)</label>
              <input
                type="number"
                value={hourlyRate}
                onChange={e => setHourlyRate(e.target.value)}
                placeholder="e.g. 400"
                min="0"
              />
            </div>
            <div className="form-row">
              <label>Contract End Date</label>
              <input
                type="date"
                value={contractEnd}
                onChange={e => setContractEnd(e.target.value)}
              />
            </div>
          </>
        )}

        <button type="button" onClick={handleSubmit} disabled={loading}>
          {loading ? "Adding..." : "Add Employee"}
        </button>

        {status && <p className="status">{status}</p>}
      </div>
    </div>
  );
}