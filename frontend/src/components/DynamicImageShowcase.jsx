import React from 'react';
import Marquee from 'react-fast-marquee';

import dest1 from '../assets/dest1.jpg';
import dest2 from '../assets/dest2.jpg';
import dest3 from '../assets/dest3.jpg';
import dest4 from '../assets/dest4.jpg';
import dest5 from '../assets/dest5.jpg';
import dest6 from '../assets/dest6.jpg';
import dest7 from '../assets/dest7.jpg';
import dest8 from '../assets/dest8.jpg';

const images = [dest1, dest2, dest3, dest4, dest5, dest6, dest7, dest8];

const WhiishWideMarquee = () => {
  return (
    <section className="bg-[#0e0e10] text-white py-16 px-4">
      <h2 className="text-3xl font-bold text-center mb-8">Explore Whiish Moments</h2>

      <Marquee speed={40} gradient={false} pauseOnHover>
        {images.map((img, i) => (
          <div
            key={i}
            className="mx-3 w-[460px] h-[300px] flex-shrink-0 bg-[#1a1a1d] rounded-xl overflow-hidden border border-[#2c2c2e] shadow-lg"
          >
            <img
              src={img}
              alt={`dest-${i}`}
              className="w-full h-full object-cover"
            />
          </div>
        ))}
      </Marquee>
    </section>
  );
};

export default WhiishWideMarquee;
