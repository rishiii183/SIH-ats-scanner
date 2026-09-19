'use client';

import React, { useState, type FC } from 'react';
import { motion, MotionConfig, type Transition } from 'framer-motion';
import { ChevronDown } from 'lucide-react';
import useMeasure from 'react-use-measure';

export interface AccordionItemData {
  id: number;
  title: string;
  icon: React.ReactNode;
  content: string;
}

interface AccordionItemProps {
  item: AccordionItemData;
  setOpenId: (id: number | null) => void;
  index: number;
  total: number;
  openIndex: number;
}

interface AccordionProps {
  items?: AccordionItemData[];
}

const springTransition: Transition = {
  type: 'spring',
  stiffness: 500,
  damping: 40,
  mass: 1,
};

const AccordionItem: FC<AccordionItemProps> = ({
  item,
  setOpenId,
  index,
  total,
  openIndex,
}) => {
  const [ref, bounds] = useMeasure();
  const isOpen = index === openIndex;

  return (
    <MotionConfig transition={springTransition}>
      <motion.li layout className="list-none w-full">
        <motion.div
          className={`overflow-hidden rounded-2xl border transition-all duration-300 ${
            isOpen
              ? 'bg-orange-50/70 border-orange-200 shadow-sm'
              : 'bg-white/80 hover:bg-white border-slate-200/80 shadow-xs hover:shadow-sm'
          }`}
        >
          <button
            type="button"
            onClick={() => setOpenId(isOpen ? null : item.id)}
            className="flex w-full cursor-pointer items-center justify-between px-4 sm:px-5 py-3.5 sm:py-4 text-left transition-colors min-h-[44px]"
          >
            <div className="flex items-center gap-3 sm:gap-3.5">
              <div className="shrink-0 flex items-center justify-center">
                {item.icon}
              </div>

              <span className="text-xs sm:text-sm font-extrabold text-slate-800">
                {item.title}
              </span>
            </div>


            <motion.div 
              animate={{ rotate: isOpen ? 180 : 0 }}
              transition={{ duration: 0.25 }}
              className="w-7 h-7 rounded-full bg-slate-100/80 flex items-center justify-center text-slate-400 shrink-0 ml-2 min-h-[28px] min-w-[28px]"
            >
              <ChevronDown className="w-4 h-4 text-slate-600" />
            </motion.div>
          </button>

          <motion.div
            initial={false}
            animate={{
              height: isOpen ? bounds.height : 0,
              opacity: isOpen ? 1 : 0,
            }}
            className="overflow-hidden"
          >
            <div ref={ref}>
              <div className="px-4 sm:px-5 pb-4 sm:pb-5 pt-1 text-xs sm:text-sm font-medium text-slate-600 leading-relaxed pl-4 sm:pl-16">
                {item.content}
              </div>
            </div>
          </motion.div>
        </motion.div>
      </motion.li>
    </MotionConfig>
  );
};

export const AccordionApp: FC<AccordionProps> = ({ items }) => {
  const defaultItems = items ?? [];
  const [openId, setOpenId] = useState<number | null>(null);
  const openIndex = defaultItems.findIndex((item) => item.id === openId);

  return (
    <div className="w-full flex flex-col items-center justify-center">
      <ul className="w-full space-y-2.5 p-0 m-0">
        {defaultItems.map((item, index) => (
          <AccordionItem
            key={item.id}
            item={item}
            setOpenId={setOpenId}
            index={index}
            total={defaultItems.length}
            openIndex={openIndex}
          />
        ))}
      </ul>
    </div>
  );
};
