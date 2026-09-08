import { User } from "lucide-react";
import { ChatMessage } from "@/lib/types";

export function ChatBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex w-full ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      <div className={`flex max-w-[90%] sm:max-w-[80%] ${isUser ? "flex-row-reverse" : "flex-row"} gap-3`}>
        
        {/* Avatar */}
        <div className={`shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? "bg-clinical-slate text-white" : "bg-clinical-teal text-white"
        }`}>
          {isUser ? <User size={16} /> : <span className="font-bold text-lg leading-none">+</span>}
        </div>
        
        {/* Message Bubble */}
        <div className={`px-4 py-3 rounded-2xl ${
          isUser 
            ? "bg-clinical-slate text-white rounded-tr-sm" 
            : "bg-white border border-gray-100 shadow-sm text-gray-800 rounded-tl-sm"
        }`}>
          {isUser ? (
            <p className="text-sm md:text-base leading-relaxed">{message.content}</p>
          ) : (
            <div 
              className="prose prose-sm md:prose-base max-w-none prose-p:my-2 prose-headings:mb-3 prose-headings:mt-4 prose-a:text-clinical-teal hover:prose-a:text-clinical-tealDark"
              dangerouslySetInnerHTML={{ __html: message.content }} 
            />
          )}
        </div>
      </div>
    </div>
  );
}
