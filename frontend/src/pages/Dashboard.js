import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Set up Axios interceptor to automatically include JWT in the Authorization header for all requests
axios.interceptors.request.use((config) => {
    const token = localStorage.getItem('jwt');
    if (token) {
        config.headers['Authorization'] = 'Bearer ' + token;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

const Dashboard = () => {
    const [userData, setUserData] = useState({});
    const [jwt, setJwt] = useState('');

    useEffect(() => {
        const token = localStorage.getItem('jwt');
        setJwt(token);
        
        // No need to manually set headers here since it's done by the interceptor
        axios.get("http://127.0.0.1:8000/business/get_user_data/")
        .then(response => {
            console.log(response);
            setUserData(response.data);
        })
        .catch(error => {
            console.error("Error fetching user data: ", error);
        });
    }, []); 

    return (
        <div style={{minHeight:'70vh', paddingTop:'2em'}}>
            <h1 style={{textAlign:'center'}}>Information from Database</h1>
            <h5 style={{textAlign:'center'}}>And real session management token</h5>
            <table style={{ border: '1px solid black', width: '50%', marginLeft:'auto', marginRight:'auto', textAlign:'center' }}>
            <thead>
                <tr>
                    <th>Key</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                {Object.entries(userData).map(([key, value], index) => (
                    <tr key={index}>
                        <td>{key}</td>
                        <td>{value}</td>
                    </tr>
                ))}
                <tr>
                    <td>Session Token</td>
                    <td style={{maxWidth:'30px', overflowWrap: 'anywhere'}}>{jwt}</td>
                </tr>
            </tbody>
        </table>
        </div>
    );
}

export default Dashboard;
