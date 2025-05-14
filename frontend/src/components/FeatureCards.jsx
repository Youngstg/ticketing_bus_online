import React from 'react';

const features = [
  {
    icon: '🚌',
    title: 'Easy Booking',
    desc: 'Book your bus ticket in just a few clicks with a streamlined process.',
  },
  {
    icon: '🎫',
    title: 'Track Tickets',
    desc: 'View your active and past tickets, and access all trip info easily.',
  },
  {
    icon: '🛡️',
    title: 'Safe Travel',
    desc: 'Travel with verified, trusted partners and protected bookings.',
  },
];

const FeatureCards = () => {
  return (
    <section className="bg-[#0e0e10] text-white px-6 py-24">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-12">
        {features.map((feature, index) => (
          <div
            key={index}
            className="bg-[#1a1a1d] p-14 rounded-3xl border border-[#2c2c2e] shadow-2xl hover:shadow-2xl transition transform hover:scale-[1.03]"
          >
            <div className="text-8xl mb-8 text-center">{feature.icon}</div>
            <h3 className="text-4xl font-bold mb-6 text-center">{feature.title}</h3>
            <p className="text-gray-400 text-xl text-center leading-relaxed">
              {feature.desc}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default FeatureCards;
