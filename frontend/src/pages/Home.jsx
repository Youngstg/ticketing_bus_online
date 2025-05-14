import React from 'react';
import HeroSection from '../components/HeroSection';
import FeatureCards from '../components/FeatureCards';
import DynamicImageShowcase from '../components/DynamicImageShowcase';

const Home = () => {
  return (
    <div className="bg-[#0e0e10] min-h-screen">
      <HeroSection />
      <FeatureCards />
      <DynamicImageShowcase />
    </div>
  );
};

export default Home;
