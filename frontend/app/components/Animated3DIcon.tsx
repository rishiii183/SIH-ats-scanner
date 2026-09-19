"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { ShieldCheck, CheckCircle2, Zap, Sparkles, Award } from 'lucide-react';

export type Icon3DVariant = 'shield' | 'check' | 'zap' | 'sparkles' | 'award';

interface Animated3DIconProps {
  variant: Icon3DVariant;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const Animated3DIcon: React.FC<Animated3DIconProps> = ({ 
  variant, 
  size = 'md',
  className = '' 
}) => {
  
  const sizeClasses = {
    sm: 'w-9 h-9 text-base',
    md: 'w-11 h-11 text-lg',
    lg: 'w-14 h-14 text-2xl',
  }[size];

  const iconSizes = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-7 h-7',
  }[size];

  // Config per 3D icon theme
  const config = {
    shield: {
      bg: 'bg-gradient-to-tr from-orange-600 via-orange-500 to-amber-400',
      border: 'border-orange-300/80',
      glow: 'shadow-[0_10px_25px_-4px_rgba(249,115,22,0.45),inset_0_2px_4px_rgba(255,255,255,0.7),inset_0_-2px_4px_rgba(0,0,0,0.2)]',
      icon: <ShieldCheck className={`${iconSizes} text-white drop-shadow-[0_2px_4px_rgba(0,0,0,0.3)]`} />,
      pulseRing: 'bg-orange-400/20 border-orange-400/40',
    },
    check: {
      bg: 'bg-gradient-to-tr from-emerald-600 via-emerald-500 to-teal-400',
      border: 'border-emerald-300/80',
      glow: 'shadow-[0_10px_25px_-4px_rgba(16,185,129,0.45),inset_0_2px_4px_rgba(255,255,255,0.7),inset_0_-2px_4px_rgba(0,0,0,0.2)]',
      icon: <CheckCircle2 className={`${iconSizes} text-white drop-shadow-[0_2px_4px_rgba(0,0,0,0.3)]`} />,
      pulseRing: 'bg-emerald-400/20 border-emerald-400/40',
    },
    zap: {
      bg: 'bg-gradient-to-tr from-amber-600 via-amber-500 to-yellow-300',
      border: 'border-amber-300/80',
      glow: 'shadow-[0_10px_25px_-4px_rgba(245,158,11,0.45),inset_0_2px_4px_rgba(255,255,255,0.7),inset_0_-2px_4px_rgba(0,0,0,0.2)]',
      icon: <Zap className={`${iconSizes} text-white drop-shadow-[0_2px_4px_rgba(0,0,0,0.3)]`} />,
      pulseRing: 'bg-amber-400/20 border-amber-400/40',
    },
    sparkles: {
      bg: 'bg-gradient-to-tr from-orange-500 via-amber-500 to-yellow-400',
      border: 'border-orange-300/80',
      glow: 'shadow-[0_10px_25px_-4px_rgba(249,115,22,0.45),inset_0_2px_4px_rgba(255,255,255,0.7),inset_0_-2px_4px_rgba(0,0,0,0.2)]',
      icon: <Sparkles className={`${iconSizes} text-white drop-shadow-[0_2px_4px_rgba(0,0,0,0.3)]`} />,
      pulseRing: 'bg-orange-400/20 border-orange-400/40',
    },
    award: {
      bg: 'bg-gradient-to-tr from-orange-600 via-amber-600 to-amber-400',
      border: 'border-amber-300/80',
      glow: 'shadow-[0_10px_25px_-4px_rgba(245,158,11,0.45),inset_0_2px_4px_rgba(255,255,255,0.7),inset_0_-2px_4px_rgba(0,0,0,0.2)]',
      icon: <Award className={`${iconSizes} text-white drop-shadow-[0_2px_4px_rgba(0,0,0,0.3)]`} />,
      pulseRing: 'bg-amber-400/20 border-amber-400/40',
    },
  }[variant];

  return (
    <div className={`relative inline-flex items-center justify-center group ${className}`}>
      {/* 3D Ambient Outer Pulse Ring */}
      <motion.div
        animate={{
          scale: [1, 1.25, 1],
          opacity: [0.35, 0.7, 0.35],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className={`absolute inset-0 rounded-2xl border ${config.pulseRing} blur-[3px] pointer-events-none`}
      />

      {/* 3D Isometric Floating Cube/Badge Container */}
      <motion.div
        whileHover={{
          scale: 1.15,
          rotateX: 12,
          rotateY: -12,
          y: -3,
        }}
        animate={{
          y: [0, -3, 0],
          rotateZ: [0, 1.5, 0, -1.5, 0],
        }}
        transition={{
          y: {
            duration: 2.6,
            repeat: Infinity,
            ease: "easeInOut",
          },
          rotateZ: {
            duration: 5,
            repeat: Infinity,
            ease: "easeInOut",
          },
          scale: { type: "spring", stiffness: 400, damping: 20 },
        }}
        style={{
          transformStyle: "preserve-3d",
          perspective: 600,
        }}
        className={`relative ${sizeClasses} rounded-2xl ${config.bg} border-t ${config.border} ${config.glow} flex items-center justify-center cursor-pointer transition-shadow`}
      >
        {/* Top 3D Specular Sheen Glare */}
        <div className="absolute top-0.5 left-1 right-1 h-[40%] bg-gradient-to-b from-white/60 via-white/20 to-transparent rounded-t-xl pointer-events-none" />

        {/* 3D Center Icon with Depth */}
        <motion.div 
          className="relative z-10 flex items-center justify-center"
          animate={{ scale: [1, 1.05, 1] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        >
          {config.icon}
        </motion.div>

        {/* Bottom 3D Bevel Darkening Layer */}
        <div className="absolute bottom-0 inset-x-0 h-1.5 bg-black/15 rounded-b-2xl pointer-events-none" />
      </motion.div>
    </div>
  );
};
