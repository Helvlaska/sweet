import Header from "./header/Header";
import NavBar from "../../../components/NavBar/NavBar";
import GlycemiaCard from "../user/cards/glycemia/Glycemia";
import ActivityCard from "../user/cards/activity/Activity";
import MedicationCard from "../user/cards/medication/Medication";
import WeightCard from "../user/cards/weight/Weight";
import MoodCard from "../user/cards/mood/Mood";
import MealCard from "../user/cards/meal/Meal";
import ArticleCard from "../user/article/Article";

function DashboardPage() {
  return (
    <div className="dashboard">
      <NavBar />
      <Header />
      <div className="dashboard__wrapper">
        <div className="dashboard__master">
          <GlycemiaCard />
          <ActivityCard />
          <MedicationCard />
          <WeightCard />
        </div>

        <div className="dashboard__option">
          <MoodCard />
          <MealCard />
        </div>
      </div>

      <ArticleCard />
    </div>
  )
}
export default DashboardPage;
