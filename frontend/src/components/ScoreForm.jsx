import React, { useState } from "react";

/* ---------- Month options ---------- */
const months = [
  "2026-01",
  "2026-02",
  "2026-03",
  "2026-04",
];

/* ---------- Initial outlet state ---------- */
const initialOutletState = {
  name: "",
  google_rating: "",
  zomato_rating: "",
  swiggy_rating: "",
  food_cost_percentage: "",
  online_activity_percentage_zomato: "",
  online_activity_percentage_swiggy: "",
  kitchen_prep_time_zomato: "",
  kitchen_prep_time_swiggy: "",
  bad_order_percentage: "",
  delay_order_percentage: "",
  outlet_audit_mistakes: "",
  total_sale: "",
  add_on_sale: "",
};

const ScoreForm = ({ onCalculate, loading }) => {
  /* ---------- General info ---------- */
  const [managerName, setManagerName] = useState("");
  const [mallName, setMallName] = useState("");
  const [month, setMonth] = useState(""); // ✅ MONTH STATE

  /* ---------- Outlet states ---------- */
  const [amritsari, setAmritsari] = useState({
    ...initialOutletState,
    name: "Amritsari Express",
  });

  const [cafe, setCafe] = useState({
    ...initialOutletState,
    name: "Cafe Chennai",
  });

  /* ---------- Helpers ---------- */
  const handleOutletChange = (setOutlet, field, value) => {
    setOutlet((prev) => ({ ...prev, [field]: value }));
  };

  const parse = (val) => (val === "" ? 0 : parseFloat(val));
  const parseIntVal = (val) => (val === "" ? 0 : parseInt(val, 10));

  const formatOutlet = (o) => ({
    name: o.name,
    google_rating: parse(o.google_rating),
    zomato_rating: parse(o.zomato_rating),
    swiggy_rating: parse(o.swiggy_rating),
    food_cost_percentage: parse(o.food_cost_percentage),
    online_activity_percentage_zomato: parse(o.online_activity_percentage_zomato),
    online_activity_percentage_swiggy: parse(o.online_activity_percentage_swiggy),
    kitchen_prep_time_zomato: parse(o.kitchen_prep_time_zomato),
    kitchen_prep_time_swiggy: parse(o.kitchen_prep_time_swiggy),
    bad_order_percentage: parse(o.bad_order_percentage),
    delay_order_percentage: parse(o.delay_order_percentage),
    outlet_audit_mistakes: parseIntVal(o.outlet_audit_mistakes),
    total_sale: parse(o.total_sale),
    add_on_sale: parse(o.add_on_sale),
  });

  /* ---------- Submit ---------- */
  const handleSubmit = (e) => {
    e.preventDefault();

    const payload = {
      manager_name: managerName,
      mall_name: mallName,
      month: month || null, // ✅ IMPORTANT
      amritsari_express: formatOutlet(amritsari),
      cafe_chennai: formatOutlet(cafe),
    };

    onCalculate(payload); // ✅ ONLY ONCE
  };

  /* ---------- Reusable input block ---------- */
  const InputSection = ({ title, field, amritsariVal, cafeVal, type = "number" }) => (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
      <div>
        <label className="block text-xs text-slate-400 mb-1">{title} (Amritsari)</label>
        <input
          type={type}
          className="input-field"
          value={amritsariVal}
          onChange={(e) =>
            handleOutletChange(setAmritsari, field, e.target.value)
          }
        />
      </div>
      <div>
        <label className="block text-xs text-slate-400 mb-1">{title} (Cafe Chennai)</label>
        <input
          type={type}
          className="input-field"
          value={cafeVal}
          onChange={(e) =>
            handleOutletChange(setCafe, field, e.target.value)
          }
        />
      </div>
    </div>
  );

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      {/* ---------- General Info ---------- */}
      <div className="card">
        <h2 className="text-xl font-bold mb-6">General Information</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="text-sm text-slate-300">Manager Name</label>
            <input
              className="input-field"
              value={managerName}
              onChange={(e) => setManagerName(e.target.value)}
              required
            />
          </div>

          <div>
            <label className="text-sm text-slate-300">Mall Name</label>
            <input
              className="input-field"
              value={mallName}
              onChange={(e) => setMallName(e.target.value)}
              required
            />
          </div>

          {/* ✅ MONTH SELECTOR */}
          <div>
            <label className="text-sm text-slate-300">Month (optional)</label>
            <select
              className="input-field"
              value={month}
              onChange={(e) => setMonth(e.target.value)}
            >
              <option value="">Testing / No Month</option>
              {months.map((m) => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* ---------- Metrics ---------- */}
      <div className="card">
        <InputSection
          title="Google Rating"
          field="google_rating"
          amritsariVal={amritsari.google_rating}
          cafeVal={cafe.google_rating}
        />

        <InputSection
          title="Food Cost %"
          field="food_cost_percentage"
          amritsariVal={amritsari.food_cost_percentage}
          cafeVal={cafe.food_cost_percentage}
        />

        <InputSection
          title="Bad Order %"
          field="bad_order_percentage"
          amritsariVal={amritsari.bad_order_percentage}
          cafeVal={cafe.bad_order_percentage}
        />

        <InputSection
          title="Delay Order %"
          field="delay_order_percentage"
          amritsariVal={amritsari.delay_order_percentage}
          cafeVal={cafe.delay_order_percentage}
        />
      </div>

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={loading}
          className="btn-primary"
        >
          {loading ? "Calculating..." : "Calculate Score"}
        </button>
      </div>
    </form>
  );
};

export default ScoreForm;