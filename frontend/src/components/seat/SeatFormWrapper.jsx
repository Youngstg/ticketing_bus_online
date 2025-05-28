import { useParams } from "react-router-dom";
import AddSeatForm from "./AddSeatForm";
import SeatList from "./SeatList";

export default function SeatFormWrapper() {
  const { scheduleId } = useParams();

  return (
    <>
      <AddSeatForm scheduleId={scheduleId} />
      <SeatList scheduleId={scheduleId} />
    </>
  );
}
