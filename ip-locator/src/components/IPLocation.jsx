import React, { useState } from 'react';
import axios from 'axios';

const IPLocation = ({ token }) => {
  const [ip, setIp] = useState('');
  const [location, setLocation] = useState('');
  const [population, setPopulation] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/api/locations/',
        { ip_address: ip },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setLocation(response.data.location);
      setPopulation(response.data.population);
    } catch (error) {
      console.error('Error fetching location!', error);
    }
  };

  return (
    <div>
      <h1>IP Location Finder</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="IP Address"
          value={ip}
          onChange={(e) => setIp(e.target.value)}
        />
        <button type="submit">Find Location</button>
      </form>
      {location && <p>Location: {location}</p>}
      {population && <p>Population: {population}</p>}
    </div>
  );
};

export default IPLocation;
